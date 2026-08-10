"""Prove that the asserting guards fail on the defect they were written to catch.

HOW-TO-DESIGN.md section 8: *"After writing a test that asserts a defect is fixed, run its measure
against the pre-fix arrangement and confirm it fails there. A gap test that reported 0 both before
and after a fix would be worse than no test at all."*

This script does exactly that. It loads the real context, injects each defect **in memory**, and
confirms the corresponding measure flips from pass to fail. Nothing on disk is modified.

Three of these are not hypothetical — they are the defects this repository actually shipped and
then fixed during Milestone 1:

* ``GRT-031`` failed when the anchorage blocks were placed *beyond* the approach dimension, making
  the bridge 258 ft too long.
* ``STT-005`` failed on a placeholder tower width of 120 ft, which is the Manhattan Bridge's deck
  width.
* ``STT-006`` failed on a placeholder truss offset of 40 ft, which is the Williamsburg Bridge's
  truss depth.

Run::

    python scripts/prove_guards.py
"""

from __future__ import annotations

import copy
import sys
from pathlib import Path
from typing import Any, Callable

sys.path.insert(0, str(Path(__file__).resolve().parent))

import validate_dimensions as vd  # noqa: E402


def _test(suite_path: Path, test_id: str) -> dict[str, Any]:
    import json

    for test in json.loads(suite_path.read_text(encoding="utf-8"))["tests"]:
        if test["id"] == test_id:
            return test
    raise KeyError(f"no test {test_id} in {suite_path.name}")


GRT = vd.REPO / "tests" / "geometry_regression_tests.json"
STT = vd.REPO / "tests" / "source_traceability_tests.json"


def defect_deck_gap(ctx: vd.Ctx) -> None:
    """Stop the deck at the anchorage face, where the SUSPENDED structure ends.

    This is the exact bug HOW-TO-DESIGN.md section 11 records as having shipped twice on the
    Manhattan Bridge, leaving the roadway terminating in mid-air.
    """
    by_id = {p["part_id"]: p for p in ctx.parts}
    by_id["deck_manhattan_anchorage_top"]["bbox_min_m"][0] -= 40.0
    by_id["deck_manhattan_anchorage_top"]["bbox_max_m"][0] -= 40.0


def defect_stale_hash(ctx: vd.Ctx) -> None:
    """Edit the control document and forget to rebuild."""
    ctx.parts_doc["control_document_sha256"] = "0" * 64


def defect_deck_too_long(ctx: vd.Ctx) -> None:
    """Place the anchorage blocks beyond the approach dimension instead of inside it."""
    by_id = {p["part_id"]: p for p in ctx.parts}
    by_id["deck_manhattan_approach"]["bbox_min_m"][0] -= 39.3192  # 129 ft


def defect_manhattan_value(ctx: vd.Ctx) -> None:
    """Let the Manhattan Bridge's 120 ft deck width in through a placeholder."""
    control = ctx.model.by_id["CTL-109"]
    object.__setattr__(control, "value", 120.0)
    object.__setattr__(control, "value_m", 120.0 * 0.3048)


def defect_williamsburg_value(ctx: vd.Ctx) -> None:
    """Let the Williamsburg Bridge's 40 ft truss depth in through a placeholder."""
    control = ctx.model.by_id["CTL-104"]
    object.__setattr__(control, "value", 40.0)
    object.__setattr__(control, "value_m", 40.0 * 0.3048)


def defect_unread_source(ctx: vd.Ctx) -> None:
    """Cite a source that is registered in the verification queue but has not been read."""
    ctx.read_sources.discard("SRC-004")


def defect_subway_track(ctx: vd.Ctx) -> None:
    """Follow the adapted brief literally and model four subway tracks."""
    ctx.parts.append(dict(ctx.parts[0], part_id="subway_track_1"))


def defect_promenade_stops_with_road(ctx: vd.Ctx) -> None:
    """End the walkway at Adams Street with the roadway.

    This is the defect the repository owner caught by eye after Milestone 1: the promenade was
    co-terminous with the road, so the Brooklyn Curve did not exist and the tourist staircase down to
    Washington Street was attached to nothing.
    """
    by_id = {p["part_id"]: p for p in ctx.parts}
    curve = by_id["promenade_brooklyn_curve"]
    curve["bbox_max_m"][0] = curve["bbox_min_m"][0] + 0.5


def defect_promenade_gap(ctx: vd.Ctx) -> None:
    """Open a hole in the walkway at the Brooklyn tower."""
    by_id = {p["part_id"]: p for p in ctx.parts}
    seg = by_id["promenade_brooklyn_side_span"]
    seg["bbox_min_m"][0] += 60.0


def defect_promenade_overlap(ctx: vd.Ctx) -> None:
    """Put the tower balcony back inside the side span, as the first build of this chain did."""
    by_id = {p["part_id"]: p for p in ctx.parts}
    by_id["promenade_brooklyn_side_span"]["bbox_min_m"][0] -= 16.6  # back to the tower centerline


def defect_cite_unreviewed_photos(ctx: vd.Ctx) -> None:
    """Cite the photograph corpus for a material before anyone has reviewed it.

    The tempting version of this mistake: MAT-010 grades the promenade decking D because no source
    says what the planks are, a corpus of 272 photographs of that decking now exists, and pointing
    the material rule at it looks like progress. It is not -- nobody has looked at them yet.
    """
    rule = ctx.model.materials[0]
    object.__setattr__(rule, "source_ids", tuple(list(rule.source_ids) + ["SRC-018"]))


def defect_saddles_never_built(ctx: vd.Ctx) -> None:
    """Register the eight saddle bearings and then never model them.

    This is the defect a reviewer caught by eye: with no saddle geometry the cable vanished into a
    solid tower block and appeared to attach tens of feet below the top, even though its elevation
    was right.
    """
    ctx.parts[:] = [p for p in ctx.parts if not p["part_id"].startswith("saddle_")]


def defect_callout_on_assumed(ctx: vd.Ctx) -> None:
    """Annotate a dimension on a part nothing locates."""
    for part in ctx.parts:
        if part["provenance"] == "ASSUMED":
            part["dimension_callouts"] = [{"label": "100 ft bent spacing"}]
            return
    raise AssertionError("no ASSUMED part to annotate — this proof needs one")


CASES: list[tuple[str, Path, str, Callable[[vd.Ctx], None]]] = [
    ("deck develops a longitudinal gap at the anchorage", GRT, "GRT-030", defect_deck_gap),
    ("the walkway stops at Adams Street with the road", GRT, "GRT-034", defect_promenade_stops_with_road),
    ("a hole opens in the walkway at the Brooklyn tower", GRT, "GRT-033", defect_promenade_gap),
    ("the tower balcony slides back inside the side span", GRT, "GRT-035", defect_promenade_overlap),
    ("control document edited without rebuilding", GRT, "GRT-001", defect_stale_hash),
    ("anchorage placed outside the approach dimension", GRT, "GRT-031", defect_deck_too_long),
    ("dimension annotated on an ASSUMED part", GRT, "GRT-070", defect_callout_on_assumed),
    ("Manhattan Bridge deck width enters as a placeholder", STT, "STT-005", defect_manhattan_value),
    ("Williamsburg truss depth enters as a placeholder", STT, "STT-006", defect_williamsburg_value),
    ("a control cites a source that was never read", STT, "STT-013", defect_unread_source),
    ("the brief's four subway tracks get modelled", STT, "STT-008", defect_subway_track),
    ("the eight sourced saddles are registered but never built", STT, "STT-015", defect_saddles_never_built),
    ("an unreviewed photo corpus is cited for a material", STT, "STT-017", defect_cite_unreviewed_photos),
]


def main() -> int:
    baseline = vd.Ctx()
    failures = 0

    print("proving the guards have teeth")
    print("-" * 78)

    # First: the parser must genuinely cope with markdown bold in the read-state cell.
    bolded = [
        line.strip().strip("|").split("|")[0].strip()
        for line in vd.SOURCE_REGISTER.read_text(encoding="utf-8").splitlines()
        if line.strip().startswith("| SRC-") and "**read**" in line
    ]
    if not bolded:
        print("  FAIL  no source row uses **read**, so the bold-parsing proof is vacuous")
        failures += 1
    elif not set(bolded) <= baseline.read_sources:
        print(f"  FAIL  read-state parser missed bolded rows: {sorted(set(bolded) - baseline.read_sources)}")
        failures += 1
    else:
        print(f"  ok    read-state parser handles markdown bold ({len(bolded)} bolded rows detected)")

    for label, suite_path, test_id, inject in CASES:
        test = _test(suite_path, test_id)
        fn = vd.MEASURES[test["rule"]]

        clean = fn(baseline, test)
        if not clean["passed"]:
            print(f"  FAIL  {test_id} does not pass on the clean model; nothing to prove")
            failures += 1
            continue

        ctx = vd.Ctx()
        ctx.parts_doc = copy.deepcopy(ctx.parts_doc)
        ctx.parts = ctx.parts_doc["parts"]
        inject(ctx)
        broken = fn(ctx, test)
        if broken["passed"]:
            print(f"  FAIL  {test_id} still passes with the defect injected — the guard is vacuous")
            print(f"        defect: {label}")
            failures += 1
        else:
            print(f"  ok    {test_id} fails on: {label}")

    print("-" * 78)
    if failures:
        print(f"{failures} guard(s) could not be proven")
        return 1
    print(f"{len(CASES) + 1} guards proven to fail on the defect they were written to catch")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
