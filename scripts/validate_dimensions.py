"""Run the geometry regression and source traceability suites.

Both suites are declared as data in ``tests/*.json``; this module supplies the measures. Three
modes are supported:

* ``assert``      — a failure fails the build.
* ``report_only`` — surfaced without blocking. Used for things that *should* change later, such as
  the MEASURED count.
* ratchets        — ``ratchet_min`` / ``ratchet_max``. Raising one requires editing the expectation
  in the JSON **and** writing the argument for it in that test's ``rationale`` field.

Run::

    python scripts/validate_dimensions.py            # run everything
    python scripts/validate_dimensions.py --json     # machine-readable summary only
"""

from __future__ import annotations

import json
import hashlib
import re
import sys
from pathlib import Path
from typing import Any, Callable

sys.path.insert(0, str(Path(__file__).resolve().parent))

from control_model import load_control_model  # noqa: E402
from normalize_units import ho_millimeters, is_linear  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
CONTROL_DOC = REPO / "GEOMETRY-CONTROL.md"
SOURCE_REGISTER = REPO / "SOURCE-REGISTER.md"
BRIEF = REPO / "AGENT-INSTRUCTIONS.md"
PARTS = REPO / "viewer" / "metadata" / "parts.json"
BUILD_REPORT = REPO / "viewer" / "metadata" / "build_report.json"
GEOMETRY = REPO / "cad" / "procedural" / "control_skeleton_geometry.json"
SUITES = (
    REPO / "tests" / "geometry_regression_tests.json",
    REPO / "tests" / "source_traceability_tests.json",
)
REPORT_OUT = REPO / "tests" / "validation_report.json"

SOURCE_ID_RE = re.compile(r"\bSRC-\d+\b")
CONTROL_ROW_RE = re.compile(r"^\|\s*CTL-\d+\s*\|", re.MULTILINE)
OPEN_QUESTION_RE = re.compile(r"^\|\s*(OQ-\d+)\s*\|", re.MULTILINE)
FT_TO_M = 0.3048
IN_TO_M = 0.0254


class Ctx:
    """Everything a measure might need, loaded once."""

    def __init__(self) -> None:
        self.model = load_control_model(CONTROL_DOC)
        self.parts_doc = json.loads(PARTS.read_text(encoding="utf-8"))
        self.parts = self.parts_doc["parts"]
        self.report = json.loads(BUILD_REPORT.read_text(encoding="utf-8"))
        self.geometry = json.loads(GEOMETRY.read_text(encoding="utf-8"))
        register_text = SOURCE_REGISTER.read_text(encoding="utf-8")
        self.register_text = register_text
        self.registered_sources = set(SOURCE_ID_RE.findall(register_text))
        self.read_sources = self._read_sources(register_text)
        self.open_questions = set(OPEN_QUESTION_RE.findall(CONTROL_DOC.read_text(encoding="utf-8")))
        self.checks = {c["id"]: c for c in self.report["derived"]["checks"]}

    @staticmethod
    def _read_sources(text: str) -> set[str]:
        """Source IDs whose register row marks them read.

        The read-state cell is written as ``**read**`` in some rows and ``read`` in others, so the
        match is made on the stripped, de-emphasised cell. Testing the test: a parser that choked on
        markdown bold would silently report every source as unread, which is exactly the failure
        recorded in HOW-TO-DESIGN.md section 11.
        """
        found: set[str] = set()
        for line in text.splitlines():
            if not line.strip().startswith("| SRC-"):
                continue
            cells = [c.strip().replace("*", "") for c in line.strip().strip("|").split("|")]
            if len(cells) < 6:
                continue
            if cells[5].lower().startswith("read"):
                found.add(cells[0])
        return found


MEASURES: dict[str, Callable[[Ctx, dict[str, Any]], dict[str, Any]]] = {}


def measure(rule: str) -> Callable[[Callable[..., dict[str, Any]]], Callable[..., dict[str, Any]]]:
    def wrap(fn: Callable[..., dict[str, Any]]) -> Callable[..., dict[str, Any]]:
        MEASURES[rule] = fn
        return fn

    return wrap


def ok(detail: str = "", **extra: Any) -> dict[str, Any]:
    return {"passed": True, "detail": detail, **extra}


def bad(detail: str, **extra: Any) -> dict[str, Any]:
    return {"passed": False, "detail": detail, **extra}


# ------------------------------------------------------------------ hash / build


@measure("control_document_hash_matches")
def _hash_parts(ctx: Ctx, _t: dict[str, Any]) -> dict[str, Any]:
    got = ctx.parts_doc.get("control_document_sha256")
    if got != ctx.model.document_sha256:
        return bad(
            f"parts.json was built from {str(got)[:12]} but GEOMETRY-CONTROL.md is now "
            f"{ctx.model.document_sha256[:12]}; rerun scripts/build_control_skeleton.py"
        )
    return ok(f"sha256 {ctx.model.document_sha256[:12]}")


@measure("geometry_hash_matches")
def _hash_geometry(ctx: Ctx, _t: dict[str, Any]) -> dict[str, Any]:
    got = ctx.geometry.get("control_document_sha256")
    if got != ctx.model.document_sha256:
        return bad(f"geometry built from {str(got)[:12]}, control document is {ctx.model.document_sha256[:12]}")
    return ok()


@measure("build_check")
def _build_check(ctx: Ctx, t: dict[str, Any]) -> dict[str, Any]:
    check = ctx.checks.get(t["check_id"])
    if check is None:
        return bad(f"build report has no check {t['check_id']}")
    detail = f"residual {check['residual_ft']:+.4f} ft (tolerance {check['tolerance_m']} m)"
    return ok(detail) if check["passed"] else bad(detail)


# ------------------------------------------------------------------- provenance


@measure("provenance_census")
def _prov_one(ctx: Ctx, t: dict[str, Any]) -> dict[str, Any]:
    n = sum(1 for p in ctx.parts if p["provenance"] == t["state"])
    return ok(f"{t['state']} = {n}", value=n, expected=t.get("expected"))


@measure("provenance_census_all")
def _prov_all(ctx: Ctx, _t: dict[str, Any]) -> dict[str, Any]:
    counts: dict[str, int] = {}
    for p in ctx.parts:
        counts[p["provenance"]] = counts.get(p["provenance"], 0) + 1
    return ok(", ".join(f"{k}={v}" for k, v in sorted(counts.items())), value=counts)


@measure("no_callout_on_assumed")
def _no_callout(ctx: Ctx, _t: dict[str, Any]) -> dict[str, Any]:
    offenders = [p["part_id"] for p in ctx.parts if p["provenance"] == "ASSUMED" and p.get("dimension_callouts")]
    if offenders:
        return bad(f"dimension callouts on ASSUMED parts: {', '.join(offenders)}")
    n = sum(1 for p in ctx.parts if p["provenance"] == "ASSUMED")
    return ok(f"{n} ASSUMED part(s), none carrying a callout")


# ------------------------------------------------------------------ deck chain


def _chain_segments(ctx: Ctx, chain_key: str = "deck_chain_ids") -> list[tuple[str, float, float]]:
    ids = ctx.report["derived"][chain_key]
    by_id = {p["part_id"]: p for p in ctx.parts}
    out = []
    for part_id in ids:
        p = by_id[part_id]
        out.append((part_id, p["bbox_min_m"][0], p["bbox_max_m"][0]))
    out.sort(key=lambda r: r[1])
    return out


def _deck_segments(ctx: Ctx) -> list[tuple[str, float, float]]:
    return _chain_segments(ctx, "deck_chain_ids")


@measure("deck_chain_continuous")
def _deck_continuous(ctx: Ctx, t: dict[str, Any]) -> dict[str, Any]:
    tol = t["tolerance_m"]
    segs = _chain_segments(ctx, t.get("chain", "deck_chain_ids"))
    gaps = []
    for (id_a, _, end_a), (id_b, start_b, _) in zip(segs, segs[1:]):
        gap = start_b - end_a
        if gap > tol:
            gaps.append(f"{gap:.3f} m between {id_a} and {id_b}")
    if gaps:
        return bad("longitudinal gap in the chain: " + "; ".join(gaps), value=gaps)
    worst = max((segs[i + 1][1] - segs[i][2]) for i in range(len(segs) - 1))
    return ok(f"{len(segs)} segments, largest joint {worst:.6f} m", value=worst)


@measure("chain_segments_do_not_overlap")
def _no_overlap(ctx: Ctx, t: dict[str, Any]) -> dict[str, Any]:
    """Neighbouring segments must abut, not overlap.

    Continuity alone does not catch this: an overlap has no gap, so GRT-030 and GRT-033 both pass
    while two slabs occupy the same space. The first promenade build put the tower balcony inside the
    side span at both ends this way.
    """
    tol = t["tolerance_m"]
    segs = _chain_segments(ctx, t["chain"])
    overlaps = []
    for (id_a, _, end_a), (id_b, start_b, _) in zip(segs, segs[1:]):
        if start_b < end_a - tol:
            overlaps.append(f"{end_a - start_b:.2f} m between {id_a} and {id_b}")
    if overlaps:
        return bad("segments overlap: " + "; ".join(overlaps))
    return ok(f"{len(segs)} segments abut cleanly")


@measure("promenade_outlasts_roadway")
def _promenade_outlasts(ctx: Ctx, t: dict[str, Any]) -> dict[str, Any]:
    """The walkway must not stop where the road stops.

    SRC-011's Brooklyn Curve carries the promenade past the roadway's Adams Street terminus, and
    SRC-012 puts its far end at Tillary and Boerum. A model whose walkway ended with the road would
    contradict three sources and, more to the point, would leave the tourist stair to DUMBO attached
    to nothing.
    """
    deck = _chain_segments(ctx, "deck_chain_ids")
    prom = _chain_segments(ctx, "promenade_chain_ids")
    overhang = prom[-1][2] - deck[-1][2]
    expected = ctx.model.m(t["control_key"])
    residual = overhang - expected
    detail = (
        f"promenade runs {overhang:.2f} m past the roadway terminus "
        f"against a sourced {expected:.2f} m (residual {residual:+.4f} m)"
    )
    return ok(detail, value=overhang) if abs(residual) <= t["tolerance_m"] else bad(detail)


@measure("deck_chain_extent")
def _deck_extent(ctx: Ctx, t: dict[str, Any]) -> dict[str, Any]:
    segs = _deck_segments(ctx)
    span = segs[-1][2] - segs[0][1]
    expected = ctx.model.m(t["control_key"])
    residual = span - expected
    detail = f"deck runs {span:.3f} m against a sourced {expected:.3f} m (residual {residual:+.4f} m)"
    return ok(detail) if abs(residual) <= t["tolerance_m"] else bad(detail)


@measure("deck_segments_nondegenerate")
def _deck_nondegenerate(ctx: Ctx, _t: dict[str, Any]) -> dict[str, Any]:
    bad_segs = [s[0] for s in _deck_segments(ctx) if s[2] - s[1] <= 0]
    if bad_segs:
        return bad(f"zero or negative length deck segments: {', '.join(bad_segs)}")
    return ok(f"{len(_deck_segments(ctx))} segments, all positive length")


# -------------------------------------------------------------------- materials


@measure("parts_have_material")
def _have_material(ctx: Ctx, _t: dict[str, Any]) -> dict[str, Any]:
    missing = [p["part_id"] for p in ctx.parts if not p.get("material")]
    return bad(f"no material on: {', '.join(missing)}") if missing else ok(f"{len(ctx.parts)} parts")


@measure("no_catchall_material")
def _no_catchall(ctx: Ctx, t: dict[str, Any]) -> dict[str, Any]:
    allowed = set(t["allowed_systems"])
    offenders = [
        p["part_id"]
        for p in ctx.parts
        if p.get("material_id") == t["catchall_material_id"] and p["system"] not in allowed
    ]
    if offenders:
        return bad(f"structural parts fell through to the catch-all rule: {', '.join(offenders)}")
    return ok()


# --------------------------------------------------------------------- ratchets


@measure("ratchet_max")
def _ratchet_max(ctx: Ctx, t: dict[str, Any]) -> dict[str, Any]:
    value = ctx.report[t["metric"]]
    detail = f"{t['metric']} = {value}, limit {t['limit']}"
    return ok(detail, value=value) if value <= t["limit"] else bad(detail, value=value)


@measure("ratchet_min")
def _ratchet_min(ctx: Ctx, t: dict[str, Any]) -> dict[str, Any]:
    value = ctx.report[t["metric"]]
    detail = f"{t['metric']} = {value}, floor {t['limit']}"
    return ok(detail, value=value) if value >= t["limit"] else bad(detail, value=value)


# --------------------------------------------------------------------- geometry


@measure("part_bbox_floor")
def _bbox_floor(ctx: Ctx, t: dict[str, Any]) -> dict[str, Any]:
    by_id = {p["part_id"]: p for p in ctx.parts}
    problems = []
    for case in t["cases"]:
        part = by_id.get(case["part_id"])
        if part is None:
            problems.append(f"{case['part_id']} missing")
            continue
        expected = -ctx.model.m(case["control_key"])
        got = part["bbox_min_m"][2]
        if abs(got - expected) > t["tolerance_m"]:
            problems.append(f"{case['part_id']} base {got:.3f} m, expected {expected:.3f} m")
    return bad("; ".join(problems)) if problems else ok(f"{len(t['cases'])} case(s)")


@measure("part_bbox_ceiling")
def _bbox_ceiling(ctx: Ctx, t: dict[str, Any]) -> dict[str, Any]:
    by_id = {p["part_id"]: p for p in ctx.parts}
    problems = []
    for case in t["cases"]:
        part = by_id.get(case["part_id"])
        if part is None:
            problems.append(f"{case['part_id']} missing")
            continue
        expected = ctx.model.m(case["control_key"])
        got = part["bbox_max_m"][2]
        if abs(got - expected) > t["tolerance_m"]:
            problems.append(f"{case['part_id']} top {got:.3f} m, expected {expected:.3f} m")
    return bad("; ".join(problems)) if problems else ok(f"{len(t['cases'])} case(s)")


@measure("file_sha256")
def _file_sha256(ctx: Ctx, t: dict[str, Any]) -> dict[str, Any]:
    """Byte-for-byte equality with a file owned by another repository.

    Deliberately hashes the raw bytes rather than comparing parsed JSON: a re-serialised copy would
    be semantically identical and would still be a contract breach, because the whole point is that
    every module in the programme carries the same bytes.
    """
    path = REPO / t["path"]
    if not path.exists():
        return bad(f"{t['path']} is missing")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != t["expected_sha256"]:
        return bad(
            f"{t['path']} sha256 {digest[:16]} does not match the canonical "
            f"{t['expected_sha256'][:16]}; copy it byte-for-byte rather than re-serialising it"
        )
    return ok(f"{t['path']} matches the canonical frame ({digest[:16]})")


@measure("ho_nonzero")
def _ho_nonzero(ctx: Ctx, _t: dict[str, Any]) -> dict[str, Any]:
    tiny = [
        c.control_id
        for c in ctx.model.controls.values()
        if is_linear(c.unit) and 0 < abs(c.value_m) and ho_millimeters(abs(c.value_m)) < 0.05
    ]
    return ok(f"{len(tiny)} control(s) below 0.05 mm at HO", value=tiny)


# ---------------------------------------------------------------- traceability


@measure("cited_sources_registered")
def _sources_registered(ctx: Ctx, _t: dict[str, Any]) -> dict[str, Any]:
    unknown = set()
    for c in ctx.model.controls.values():
        unknown |= {s for s in c.source_ids if s not in ctx.registered_sources}
    for rule in ctx.model.materials:
        unknown |= {s for s in rule.source_ids if s not in ctx.registered_sources}
    if unknown:
        return bad(f"cited but not registered: {', '.join(sorted(unknown))}")
    return ok(f"{len(ctx.registered_sources)} source IDs registered")


@measure("cited_sources_are_read")
def _sources_read(ctx: Ctx, _t: dict[str, Any]) -> dict[str, Any]:
    unread: dict[str, list[str]] = {}
    for c in ctx.model.controls.values():
        for s in c.source_ids:
            if s not in ctx.read_sources:
                unread.setdefault(s, []).append(c.control_id)
    if unread:
        return bad(
            "controls cite sources that are registered but not read: "
            + "; ".join(f"{s} ({len(v)} controls)" for s, v in sorted(unread.items()))
        )
    return ok(f"{len(ctx.read_sources)} read sources: {', '.join(sorted(ctx.read_sources))}")


@measure("graded_controls_have_sources")
def _graded_sourced(ctx: Ctx, _t: dict[str, Any]) -> dict[str, Any]:
    offenders = [c.control_id for c in ctx.model.controls.values() if c.confidence != "D" and not c.source_ids]
    return bad(f"graded but sourceless: {', '.join(offenders)}") if offenders else ok()


@measure("placeholders_have_no_sources")
def _placeholders_unsourced(ctx: Ctx, _t: dict[str, Any]) -> dict[str, Any]:
    offenders = [c.control_id for c in ctx.model.placeholders if c.source_ids]
    return bad(f"placeholders citing sources: {', '.join(offenders)}") if offenders else ok(
        f"{len(ctx.model.placeholders)} placeholders, none sourced"
    )


@measure("part_control_refs_resolve")
def _refs_resolve(ctx: Ctx, _t: dict[str, Any]) -> dict[str, Any]:
    unknown = set()
    for p in ctx.parts:
        unknown |= {r for r in p["control_refs"] if r not in ctx.model.by_id}
    return bad(f"unresolved control refs: {', '.join(sorted(unknown))}") if unknown else ok()


@measure("open_questions_registered")
def _oq_registered(ctx: Ctx, _t: dict[str, Any]) -> dict[str, Any]:
    unknown = set()
    for p in ctx.parts:
        unknown |= {q for q in p.get("open_questions", []) if q not in ctx.open_questions}
    if unknown:
        return bad(f"parts cite unregistered open questions: {', '.join(sorted(unknown))}")
    return ok(f"{len(ctx.open_questions)} open questions registered")


@measure("parts_have_source_basis")
def _have_basis(ctx: Ctx, _t: dict[str, Any]) -> dict[str, Any]:
    offenders = [p["part_id"] for p in ctx.parts if not p.get("source_basis")]
    return bad(f"no source_basis: {', '.join(offenders)}") if offenders else ok()


@measure("forbidden_source_basis")
def _forbidden_basis(ctx: Ctx, t: dict[str, Any]) -> dict[str, Any]:
    forbidden = set(t["forbidden"])
    offenders = [p["part_id"] for p in ctx.parts if forbidden & set(p["source_basis"])]
    return bad(f"forbidden source_basis on: {', '.join(offenders)}") if offenders else ok()


@measure("parts_have_required_fields")
def _required_fields(ctx: Ctx, t: dict[str, Any]) -> dict[str, Any]:
    problems = []
    for p in ctx.parts:
        missing = [f for f in t["required"] if f not in p or p[f] in (None, "", [])]
        if missing:
            problems.append(f"{p['part_id']}: {', '.join(missing)}")
    return bad("; ".join(problems[:5])) if problems else ok(f"{len(ctx.parts)} parts complete")


@measure("negative_control_values")
def _negative_control(ctx: Ctx, t: dict[str, Any]) -> dict[str, Any]:
    exempt = set(t.get("exempt_control_ids", []))
    forbidden_m = {round(v * FT_TO_M, 6) for v in t.get("forbidden_values_ft", [])}
    forbidden_m |= {round(v * IN_TO_M, 6) for v in t.get("forbidden_values_in", [])}
    forbidden_counts = set(t.get("forbidden_values_ft", []))
    hits = []
    for c in ctx.model.controls.values():
        if c.control_id in exempt:
            continue
        if is_linear(c.unit) and round(c.value_m, 6) in forbidden_m:
            hits.append(f"{c.control_id} ({c.key} = {c.value} {c.unit})")
        elif c.unit == "count" and c.value in forbidden_counts:
            hits.append(f"{c.control_id} ({c.key} = {c.value} {c.unit})")
    if hits:
        return bad(
            f"negative control {t['source']} breached — a neighbouring bridge's dimension is in "
            f"this model: {'; '.join(hits)}"
        )
    return ok(f"{len(forbidden_m)} forbidden value(s) checked against {len(ctx.model.controls)} controls")


@measure("single_control_authority")
def _single_authority(ctx: Ctx, t: dict[str, Any]) -> dict[str, Any]:
    text = (REPO / t["document"]).read_text(encoding="utf-8")
    rows = CONTROL_ROW_RE.findall(text)
    if rows:
        return bad(f"{t['document']} carries {len(rows)} CTL- row(s); GEOMETRY-CONTROL.md is the only authority")
    return ok(f"{t['document']} carries no control rows")


@measure("forbidden_part_substrings")
def _forbidden_parts(ctx: Ctx, t: dict[str, Any]) -> dict[str, Any]:
    offenders = [
        p["part_id"]
        for p in ctx.parts
        if any(s in p["part_id"].lower() for s in t["forbidden"])
    ]
    if offenders:
        return bad(f"negative control {t['source']} breached: {', '.join(offenders)}")
    return ok(f"none of {len(t['forbidden'])} forbidden substrings appears in {len(ctx.parts)} part IDs")


@measure("sourced_controls_unused_census")
def _unused_census(ctx: Ctx, _t: dict[str, Any]) -> dict[str, Any]:
    """Which sourced controls no part references.

    Not a failure: plenty of controls are recorded for traceability and deliberately not used
    (CTL-021, the superseded tower height, must never reach geometry). But this census is how the
    missing saddles were found -- CTL-046 was grade A, and nothing in the model used it.
    """
    used: set[str] = set()
    for p in ctx.parts:
        used.update(p["control_refs"])
    unused = sorted(
        c.control_id for c in ctx.model.controls.values() if not c.is_placeholder and c.control_id not in used
    )
    return ok(f"{len(unused)} sourced controls carry no geometry", value=unused)


@measure("controls_must_have_geometry")
def _must_have_geometry(ctx: Ctx, t: dict[str, Any]) -> dict[str, Any]:
    """Named controls that describe a physical element must actually be built."""
    used: set[str] = set()
    for p in ctx.parts:
        used.update(p["control_refs"])
    missing = [c for c in t["control_ids"] if c not in used]
    if missing:
        return bad(
            "sourced element(s) registered but never modelled: "
            + ", ".join(f"{c} ({ctx.model.by_id[c].key})" for c in missing if c in ctx.model.by_id)
        )
    return ok(f"{len(t['control_ids'])} structural counts all carry geometry")


@measure("unreviewed_photo_corpus_not_cited")
def _photos_not_cited(ctx: Ctx, t: dict[str, Any]) -> dict[str, Any]:
    """A photograph corpus may not grade anything until a person has reviewed it.

    SRC-018 is harvested and licence-checked but every record is `auto_screened` -- nobody has
    looked. Citing it in that state would be the exact over-claim the register warns about, and it
    would be easy to do by accident because the source row exists and looks complete.
    """
    survey_path = REPO / t["survey"]
    sid = t["source_id"]
    citing = [c.control_id for c in ctx.model.controls.values() if sid in c.source_ids]
    citing += [r.material_id for r in ctx.model.materials if sid in r.source_ids]

    if not survey_path.exists():
        return ok(f"{sid} has no survey yet; {len(citing)} rows cite it") if not citing else bad(
            f"{sid} is cited by {', '.join(citing)} but no survey exists")

    survey = json.loads(survey_path.read_text(encoding="utf-8"))
    obs = survey.get("observations", [])
    accepted = [o for o in obs if o.get("review", {}).get("status") == "accepted"]
    if not accepted and citing:
        return bad(
            f"{sid} is cited by {', '.join(citing)} but none of its {len(obs)} photographs "
            "has been reviewed by a person -- every record is still auto_screened"
        )
    return ok(f"{len(obs)} photographs, {len(accepted)} reviewed; {len(citing)} control/material rows cite {sid}")


@measure("grade_census")
def _grade_census(ctx: Ctx, _t: dict[str, Any]) -> dict[str, Any]:
    counts: dict[str, int] = {}
    for c in ctx.model.controls.values():
        counts[c.confidence] = counts.get(c.confidence, 0) + 1
    return ok(", ".join(f"{k}={v}" for k, v in sorted(counts.items())), value=counts)


# ------------------------------------------------------------------------- run


def run() -> tuple[int, dict[str, Any]]:
    ctx = Ctx()
    results: list[dict[str, Any]] = []
    failures = 0

    for suite_path in SUITES:
        suite = json.loads(suite_path.read_text(encoding="utf-8"))
        print(f"\n{suite['suite']}  ({suite_path.name})")
        print("-" * 78)
        for test in suite["tests"]:
            rule = test["rule"]
            fn = MEASURES.get(rule)
            if fn is None:
                outcome = bad(f"no measure implements rule {rule!r}")
            else:
                try:
                    outcome = fn(ctx, test)
                except Exception as exc:  # noqa: BLE001 - a broken measure is a failure
                    outcome = bad(f"measure raised {type(exc).__name__}: {exc}")
            mode = test.get("mode", "assert")
            blocking = mode == "assert"
            passed = outcome["passed"]
            if blocking and not passed:
                failures += 1
                status = "FAIL"
            elif not blocking:
                status = "note" if passed else "NOTE"
            else:
                status = "ok"
            print(f"  {status:<4} {test['id']:<8} {test['title']}")
            if outcome.get("detail"):
                print(f"       {outcome['detail']}")
            results.append(
                {
                    "suite": suite["suite"],
                    "id": test["id"],
                    "title": test["title"],
                    "rule": rule,
                    "mode": mode,
                    "passed": passed,
                    "detail": outcome.get("detail", ""),
                    "value": outcome.get("value"),
                }
            )

    summary = {
        "control_document_sha256": ctx.model.document_sha256,
        "tests_total": len(results),
        "asserting": sum(1 for r in results if r["mode"] == "assert"),
        "report_only": sum(1 for r in results if r["mode"] != "assert"),
        "failures": failures,
        "results": results,
    }
    # newline="\n" so the report is byte-identical on every platform; see _write_json in
    # build_control_skeleton.py.
    with REPORT_OUT.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(summary, indent=2) + "\n")
    print("\n" + "-" * 78)
    print(
        f"{summary['tests_total']} tests: {summary['asserting']} asserting, "
        f"{summary['report_only']} report-only, {failures} failing"
    )
    return (1 if failures else 0), summary


if __name__ == "__main__":
    code, payload = run()
    if "--json" in sys.argv:
        print(json.dumps({k: v for k, v in payload.items() if k != "results"}, indent=2))
    raise SystemExit(code)
