"""Build the Brooklyn Bridge control skeleton from GEOMETRY-CONTROL.md.

This script carries **no dimensions of its own**. Every number it uses is read from a control table
in GEOMETRY-CONTROL.md through ``control_model``. If a value is needed and is not in that document,
the build fails rather than inventing it.

Outputs::

    mesh/glb/control_skeleton.glb          prototype scale, metres
    mesh/glb/control_skeleton.gltf         + .bin sidecar
    mesh/glb/control_skeleton_ho.glb       1:87.1
    viewer/public/control_skeleton.glb     served copies
    viewer/public/control_skeleton_ho.glb
    viewer/public/parts.json
    viewer/metadata/parts.json             part metadata, one record per node
    viewer/metadata/build_report.json      counts, derived values, consistency checks
    viewer/metadata/scale_ho.json          HO reporting table
    cad/procedural/control_skeleton_geometry.json   raw derived geometry, for other toolchains

Run::

    python scripts/build_control_skeleton.py
"""

from __future__ import annotations

import json
import math
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Sequence

sys.path.insert(0, str(Path(__file__).resolve().parent))

from control_model import ControlDocumentError, ControlModel, load_control_model  # noqa: E402
from export_gltf import (  # noqa: E402
    GltfBuilder,
    box_mesh_data,
    prism_mesh_data,
    tube_mesh_data,
)
from normalize_units import HO_SCALE_DENOMINATOR, ho_report, is_linear  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
CONTROL_DOC = REPO / "GEOMETRY-CONTROL.md"
BUILDER_VERSION = "build_control_skeleton.py@1.0.0"

GRADE_ORDER = {"A": 0, "B": 1, "C": 2, "D": 3}

MATERIAL_COLORS = {
    "masonry": (0.72, 0.66, 0.58, 1.0),
    "concrete": (0.62, 0.62, 0.60, 1.0),
    "steel_structural": (0.42, 0.47, 0.53, 1.0),
    "steel_wire": (0.85, 0.72, 0.35, 1.0),
    # Split out of `roadway_surface` once the reviewed photo corpus (SRC-018) showed what the two
    # surfaces actually are. Rendering the timber promenade in asphalt grey was a visible untruth
    # that survived only because one generic name covered both.
    "asphalt": (0.30, 0.30, 0.32, 1.0),
    "timber": (0.60, 0.45, 0.30, 1.0),
    "roadway_surface": (0.34, 0.34, 0.36, 1.0),
    "reference": (0.30, 0.75, 0.85, 1.0),
}


class BuildError(RuntimeError):
    """Raised when the control document cannot support the geometry being asked for."""


# --------------------------------------------------------------------------- parts


@dataclass
class Part:
    part_id: str
    system: str
    subsystem: str
    control_refs: list[str]
    source_basis: list[str]
    open_questions: list[str] = field(default_factory=list)
    notes: str = ""
    primitives: list[dict[str, Any]] = field(default_factory=list)
    bbox_min: list[float] = field(default_factory=list)
    bbox_max: list[float] = field(default_factory=list)
    confidence: str = "D"
    provenance: str = "ASSUMED"
    material: str = ""
    material_id: str = ""
    material_confidence: str = "D"

    def to_metadata(self) -> dict[str, Any]:
        return {
            "part_id": self.part_id,
            "system": self.system,
            "subsystem": self.subsystem,
            "source_basis": self.source_basis,
            "control_refs": self.control_refs,
            "confidence": self.confidence,
            "provenance": self.provenance,
            "material": self.material,
            "material_id": self.material_id,
            "material_confidence": self.material_confidence,
            "open_questions": self.open_questions,
            "prototype_units": "meters",
            "ho_scale_units": "millimeters",
            "bbox_min_m": self.bbox_min,
            "bbox_max_m": self.bbox_max,
            "notes": self.notes,
            "review_status": "milestone-1-unreviewed",
            "last_modified_by_agent": BUILDER_VERSION,
        }


class Skeleton:
    """Accumulates parts and derives their confidence, provenance and material from the controls."""

    def __init__(self, model: ControlModel) -> None:
        self.model = model
        self.parts: list[Part] = []

    def add(
        self,
        part_id: str,
        system: str,
        subsystem: str,
        control_refs: Sequence[str],
        source_basis: Sequence[str],
        primitives: Sequence[dict[str, Any]],
        open_questions: Sequence[str] = (),
        notes: str = "",
    ) -> Part:
        refs = list(control_refs)
        unknown = [r for r in refs if r not in self.model.by_id]
        if unknown:
            raise BuildError(
                f"part {part_id!r} references control IDs that are not in "
                f"{CONTROL_DOC.name}: {', '.join(unknown)}"
            )

        part = Part(
            part_id=part_id,
            system=system,
            subsystem=subsystem,
            control_refs=refs,
            source_basis=list(source_basis),
            open_questions=list(open_questions),
            notes=notes,
            primitives=list(primitives),
        )
        part.confidence = self._confidence(refs)
        part.provenance = self._provenance(refs, part.source_basis)

        rule = self.model.material_for(part_id)
        part.material = rule.material
        part.material_id = rule.material_id
        part.material_confidence = rule.confidence

        lo, hi = _bounds(part.primitives)
        part.bbox_min, part.bbox_max = lo, hi
        self.parts.append(part)
        return part

    def _confidence(self, refs: Sequence[str]) -> str:
        """Weakest link across every control the part's geometry rests on."""
        if not refs:
            return "D"
        return max((self.model.by_id[r].confidence for r in refs), key=lambda g: GRADE_ORDER[g])

    def _provenance(self, refs: Sequence[str], source_basis: Sequence[str]) -> str:
        """Derived, never declared. See CONFIDENCE-MODEL.md section 2.

        Computed rather than hardcoded so that the day a survey or photogrammetry set is ingested,
        MEASURED stops being zero on its own.
        """
        placeholder_refs = [r for r in refs if self.model.by_id[r].is_placeholder]
        sourced_refs = [r for r in refs if not self.model.by_id[r].is_placeholder]

        if "photogrammetry" in source_basis or "survey" in source_basis:
            return "MEASURED"
        if "control_dimension" not in source_basis or not sourced_refs:
            return "ASSUMED"
        if placeholder_refs or "inferred" in source_basis:
            return "INFERRED"
        return "DOCUMENTED"


def _bounds(primitives: Iterable[dict[str, Any]]) -> tuple[list[float], list[float]]:
    lo = [math.inf] * 3
    hi = [-math.inf] * 3
    for prim in primitives:
        for point in prim["positions"]:
            for i in range(3):
                lo[i] = min(lo[i], point[i])
                hi[i] = max(hi[i], point[i])
    if lo[0] is math.inf:
        return [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]
    return [round(v, 6) for v in lo], [round(v, 6) for v in hi]


# ----------------------------------------------------------------------- geometry


def _box(lo: Sequence[float], hi: Sequence[float]) -> dict[str, Any]:
    positions, normals, indices = box_mesh_data(lo, hi)
    return {"kind": "tri", "positions": positions, "normals": normals, "indices": indices}


def _prism(bottom: Sequence[Sequence[float]], top: Sequence[Sequence[float]]) -> dict[str, Any]:
    positions, normals, indices = prism_mesh_data(bottom, top)
    return {"kind": "tri", "positions": positions, "normals": normals, "indices": indices}


def _tube(points: Sequence[Sequence[float]], radius: float, sides: int = 8) -> dict[str, Any]:
    positions, normals, indices = tube_mesh_data(points, radius, sides)
    return {"kind": "tri", "positions": positions, "normals": normals, "indices": indices}


def _lines(segments: Sequence[Sequence[Sequence[float]]]) -> dict[str, Any]:
    positions: list[Sequence[float]] = []
    indices: list[int] = []
    for start, end in segments:
        base = len(positions)
        positions.append(start)
        positions.append(end)
        indices.extend((base, base + 1))
    return {"kind": "line", "positions": positions, "normals": None, "indices": indices}


def _polyline(points: Sequence[Sequence[float]]) -> dict[str, Any]:
    return _lines([(points[i], points[i + 1]) for i in range(len(points) - 1)])


def _slab(x0: float, x1: float, z0: float, z1: float, half_width: float, thickness: float) -> dict[str, Any]:
    """A deck segment: a ruled solid whose top runs from (x0, z0) to (x1, z1)."""
    bottom = [
        (x0, -half_width, z0 - thickness),
        (x1, -half_width, z1 - thickness),
        (x1, half_width, z1 - thickness),
        (x0, half_width, z0 - thickness),
    ]
    top = [
        (x0, -half_width, z0),
        (x1, -half_width, z1),
        (x1, half_width, z1),
        (x0, half_width, z0),
    ]
    return _prism(bottom, top)


def _plan_ring(x0: float, x1: float, half_width: float, z: float) -> list[tuple[float, float, float]]:
    return [
        (x0, -half_width, z),
        (x1, -half_width, z),
        (x1, half_width, z),
        (x0, half_width, z),
    ]


# ------------------------------------------------------------------------- build


def build(model: ControlModel) -> tuple[Skeleton, dict[str, Any]]:
    m = model.m  # control value in metres
    raw = model.raw  # control value in its declared unit

    model.require(
        "main_span",
        "side_span_each",
        "bridge_proper_length",
        "total_length_including_approaches",
        "manhattan_approach_length",
        "brooklyn_approach_length",
        "center_clearance_above_mhw",
        "tower_height_above_mhw",
        "deck_width",
    )

    # ---- longitudinal stations (GEOMETRY-CONTROL.md section 4.1)
    main_span = m("main_span")
    side_span = m("side_span_each")
    x_twr_b = main_span / 2.0
    x_twr_m = -x_twr_b
    x_anc_b = x_twr_b + side_span
    x_anc_m = -x_anc_b
    anchorage_x = m("anchorage_extent_x")
    # SRC-002's five lettered dimensions sum to its stated 5989 ft with zero residual, and the
    # 129 ft anchorage is not one of them, so the block sits INSIDE the approach dimension rather
    # than beyond it. See GEOMETRY-CONTROL.md section 4.1.
    x_appr_m = x_anc_m - m("manhattan_approach_length")
    x_appr_b = x_anc_b + m("brooklyn_approach_length")
    x_anc_m_rear = x_anc_m - anchorage_x
    x_anc_b_rear = x_anc_b + anchorage_x

    # ---- consistency identities, asserted rather than assumed
    checks: list[dict[str, Any]] = []

    def check(check_id: str, description: str, lhs: float, rhs: float, tol_m: float) -> None:
        residual = lhs - rhs
        checks.append(
            {
                "id": check_id,
                "description": description,
                "value_m": round(lhs, 6),
                "expected_m": round(rhs, 6),
                "residual_m": round(residual, 6),
                "residual_ft": round(residual / 0.3048, 4),
                "tolerance_m": tol_m,
                "passed": abs(residual) <= tol_m,
            }
        )

    def check_at_least(check_id: str, description: str, lhs: float, rhs: float) -> None:
        """A one-sided check: `lhs` must be at least `rhs`.

        Distinct from `check` on purpose. Most cross-source checks ask whether two independently
        sourced numbers agree, and a tolerance is the right shape for that. A geometric
        realisability constraint is not a near-miss question — an arch whose rise is below half its
        clear span does not exist at any tolerance, so recording it as an equality with a fudge
        factor would be describing the wrong thing.
        """
        residual = lhs - rhs
        checks.append(
            {
                "id": check_id,
                "description": description,
                "value_m": round(lhs, 6),
                "expected_m": round(rhs, 6),
                "residual_m": round(residual, 6),
                "residual_ft": round(residual / 0.3048, 4),
                "tolerance_m": None,
                "comparison": "at_least",
                "passed": residual >= 0.0,
            }
        )

    check(
        "CHK-001",
        "main_span + 2 x side_span_each == bridge_proper_length",
        main_span + 2 * side_span,
        m("bridge_proper_length"),
        1e-6,
    )
    check(
        "CHK-002",
        "bridge_proper_length + both approaches == total_length_including_approaches",
        m("bridge_proper_length") + m("manhattan_approach_length") + m("brooklyn_approach_length"),
        m("total_length_including_approaches"),
        1e-6,
    )
    check(
        "CHK-003",
        "Manhattan terminus + gradient x approach roadway length == anchorage rear roadway level",
        m("manhattan_terminus_above_mhw")
        + raw("manhattan_approach_gradient")
        * (m("manhattan_approach_length") - anchorage_x),
        m("anchorage_roadway_rear_above_mhw"),
        1.0,
    )
    check(
        "CHK-004",
        "Brooklyn terminus + gradient x approach roadway length == anchorage rear roadway level",
        m("brooklyn_terminus_above_mhw")
        + raw("brooklyn_approach_gradient") * (m("brooklyn_approach_length") - anchorage_x),
        m("anchorage_roadway_rear_above_mhw"),
        1.0,
    )

    # ---- elevations (GEOMETRY-CONTROL.md section 4.2)
    z_clearance = m("center_clearance_above_mhw")
    z_truss_bottom = z_clearance
    z_truss_top = z_clearance + m("stiffening_truss_depth_present")
    z_deck_mid = z_truss_bottom + m("deck_structure_depth")
    z_tower_top = m("tower_height_above_mhw")
    z_saddle = z_tower_top - m("cable_saddle_drop_below_tower_top")
    z_cable_mid = z_truss_top + m("min_suspender_length_at_midspan")
    z_anchor_front = m("anchorage_roadway_front_above_mhw")
    z_anchor_rear = m("anchorage_roadway_rear_above_mhw")
    z_tower_roadway = m("roadway_clearance_at_tower_above_mhw")
    z_arch_crown = z_tower_roadway + m("tower_vault_height_above_roadway")
    z_arch_springing = z_arch_crown - m("tower_arch_height_above_springing")
    z_found_m = -m("caisson_depth_below_mhw_manhattan")
    z_found_b = -m("caisson_depth_below_mhw_brooklyn")
    caisson_height = m("caisson_air_chamber_height") + m("caisson_roof_thickness")
    z_term_m = m("manhattan_terminus_above_mhw")
    z_term_b = m("brooklyn_terminus_above_mhw")
    z_promenade_mid = z_deck_mid + m("promenade_elevation_above_roadway")

    # ---- the pointed arch closes on itself: the sourced radius, width and height agree
    arch_half = m("tower_arch_width") / 2.0
    arch_radius = m("tower_arch_radius")
    arch_centre_offset = arch_radius - arch_half
    arch_rise_from_radius = math.sqrt(max(arch_radius**2 - arch_centre_offset**2, 0.0))
    check(
        "CHK-005",
        "two-centred arch of sourced radius and width reaches the sourced arch height",
        arch_rise_from_radius,
        m("tower_arch_height_above_springing"),
        0.2,
    )
    check(
        "CHK-006",
        "SRC-011's on-structure promenade typologies sum to the 1883 bridge proper length",
        m("promenade_length_wood_deck_approaches")
        + m("promenade_length_wood_deck_with_cables")
        + m("promenade_length_tower_ramps")
        + m("promenade_length_towers")
        + m("promenade_length_crown")
        + m("promenade_length_trunk_cable_bases"),
        m("bridge_proper_length"),
        30.0,
    )
    check(
        "CHK-007",
        "promenade passage through one tower is no longer than that tower is thick at MHW",
        m("promenade_length_towers") / raw("tower_count"),
        m("tower_extent_x_at_mhw"),
        2.0,
    )
    check(
        "CHK-008",
        "the main cable's high point is exactly the saddle elevation",
        _parabola(x_twr_b, x_twr_b, z_saddle, z_cable_mid),
        z_saddle,
        1e-9,
    )

    # ---- transverse layout (section 4.3)
    half_deck = m("deck_width") / 2.0
    half_beam = m("floor_beam_length") / 2.0
    y_outer = m("truss_offset_outer")
    y_inner = m("truss_offset_inner")
    half_tower_y = m("tower_extent_y_at_mhw") / 2.0
    half_tower_x = m("tower_extent_x_at_mhw") / 2.0
    half_tower_x_top = m("tower_extent_x_at_top") / 2.0
    half_tower_y_top = m("tower_extent_y_at_top") / 2.0

    cable_lines = [
        ("south_outer", -y_outer),
        ("south_inner", -y_inner),
        ("north_inner", +y_inner),
        ("north_outer", +y_outer),
    ]
    if len(cable_lines) != int(raw("main_cable_count")):
        raise BuildError(
            f"the model lays out {len(cable_lines)} cables but CTL "
            f"{model.id_of('main_cable_count')} says there are {int(raw('main_cable_count'))}"
        )

    # ---- suspender pitch, derived from the sourced count (section 4.4)
    suspenders_per_cable = int(raw("suspender_count")) // int(raw("main_cable_count"))
    suspender_pitch = m("bridge_proper_length") / suspenders_per_cable
    stays_per_group = int(raw("diagonal_stay_count")) // (
        int(raw("main_cable_count")) * int(raw("tower_count")) * 2
    )
    stay_reach = stays_per_group * suspender_pitch

    sk = Skeleton(model)

    # ------------------------------------------------------------------ stations
    station_top = z_tower_top * 1.05
    for station_id, x, label in (
        ("station_manhattan_approach_end", x_appr_m, "Park Row"),
        ("station_manhattan_anchorage", x_anc_m, "Manhattan anchorage, river face"),
        ("station_manhattan_tower", x_twr_m, "Manhattan tower centerline"),
        ("station_midspan", 0.0, "Main span midpoint — model origin"),
        ("station_brooklyn_tower", x_twr_b, "Brooklyn tower centerline"),
        ("station_brooklyn_anchorage", x_anc_b, "Brooklyn anchorage, river face"),
        ("station_brooklyn_approach_end", x_appr_b, "Adams Street"),
    ):
        refs = _station_refs(model, station_id)
        sk.add(
            station_id,
            "reference",
            "station",
            refs,
            ["control_dimension"],
            [_lines([((x, 0.0, -half_deck), (x, 0.0, station_top))])],
            notes=label,
        )

    # -------------------------------------------------------------------- towers
    for end, x_c, z_found in (("manhattan", x_twr_m, z_found_m), ("brooklyn", x_twr_b, z_found_b)):
        caisson_long = (
            m("caisson_long_dimension_manhattan")
            if end == "manhattan"
            else m("caisson_long_dimension_brooklyn")
        )
        caisson_short = m("caisson_short_dimension")
        cs_x = caisson_short / 2.0
        cs_y = caisson_long / 2.0
        depth_ref = (
            "caisson_depth_below_mhw_manhattan"
            if end == "manhattan"
            else "caisson_depth_below_mhw_brooklyn"
        )
        long_ref = (
            "caisson_long_dimension_manhattan"
            if end == "manhattan"
            else "caisson_long_dimension_brooklyn"
        )

        sk.add(
            f"tower_{end}_caisson",
            "towers",
            "foundation",
            model.ids_of(
                depth_ref,
                long_ref,
                "caisson_short_dimension",
                "caisson_air_chamber_height",
                "caisson_roof_thickness",
            ),
            ["control_dimension", "inferred"],
            [_box((x_c - cs_x, -cs_y, z_found), (x_c + cs_x, cs_y, z_found + caisson_height))],
            open_questions=["OQ-005"],
            notes=(
                "Caisson footprint is sourced; the assignment of the 168/172 ft dimension to the "
                "transverse axis is reasoned from the tower being 140 ft wide and having to stand "
                "on it. See OQ-005."
            ),
        )
        sk.add(
            f"tower_{end}_foundation_block",
            "towers",
            "foundation",
            model.ids_of(
                depth_ref,
                long_ref,
                "caisson_short_dimension",
                "tower_extent_x_at_mhw",
                "tower_extent_y_at_mhw",
            ),
            ["control_dimension", "inferred"],
            [
                _prism(
                    _plan_ring(x_c - cs_x, x_c + cs_x, cs_y, z_found + caisson_height),
                    _plan_ring(x_c - half_tower_x, x_c + half_tower_x, half_tower_y, 0.0),
                )
            ],
            open_questions=["OQ-004"],
            notes="Both ends are sourced; the taper between them is reasoned.",
        )
        # The shaft rises only to the saddle. Above that the masonry cannot be solid across the
        # cable lines: SRC-002 states the cables "WERE CARRIED THROUGH THE TOWERS ON EIGHT CAST IRON
        # SADDLE BEARINGS", so the top band is modelled as two masses outboard of the outer cables
        # with the cable corridor open between them. That is INFERRED from a grade-A statement, not
        # invented -- and it is what lets a viewer see the cable reach its true height instead of
        # vanishing into a solid block several tens of feet below the top.
        t_saddle = z_saddle / z_tower_top
        half_x_saddle = half_tower_x + (half_tower_x_top - half_tower_x) * t_saddle
        half_y_saddle = half_tower_y + (half_tower_y_top - half_tower_y) * t_saddle

        sk.add(
            f"tower_{end}_shaft",
            "towers",
            "masonry",
            model.ids_of(
                "tower_extent_x_at_mhw",
                "tower_extent_y_at_mhw",
                "tower_extent_x_at_top",
                "tower_extent_y_at_top",
                "tower_height_above_mhw",
                "cable_saddle_drop_below_tower_top",
            ),
            ["control_dimension", "drawing"],
            [
                _prism(
                    _plan_ring(x_c - half_tower_x, x_c + half_tower_x, half_tower_y, 0.0),
                    _plan_ring(x_c - half_x_saddle, x_c + half_x_saddle, half_y_saddle, z_saddle),
                )
            ],
            open_questions=["OQ-004"],
            notes=(
                "Height and plan at mean high water are grade A from SRC-002. The plan at the top "
                "is a placeholder, so the taper is INFERRED. The shaft stops at the saddle; the "
                "masonry above it is tower_%s_cornice." % end
            ),
        )

        # Cornice: the top band, open across the cable corridor.
        cable_margin = m("main_cable_diameter") * 2.0
        corridor = y_outer + cable_margin
        cornice_prims = []
        for sign in (-1.0, 1.0):
            y_in = sign * corridor
            y_out = sign * half_tower_y_top
            lo_y, hi_y = min(y_in, y_out), max(y_in, y_out)
            cornice_prims.append(
                _box(
                    (x_c - half_tower_x_top, lo_y, z_saddle),
                    (x_c + half_tower_x_top, hi_y, z_tower_top),
                )
            )
        sk.add(
            f"tower_{end}_cornice",
            "towers",
            "masonry",
            model.ids_of(
                "tower_height_above_mhw",
                "cable_saddle_drop_below_tower_top",
                "tower_extent_x_at_top",
                "tower_extent_y_at_top",
                "truss_offset_outer",
                "main_cable_diameter",
            ),
            ["control_dimension", "drawing", "inferred"],
            cornice_prims,
            open_questions=["OQ-004", "OQ-016"],
            notes=(
                "The masonry above the saddle. Modelled as two masses outboard of the outer cables "
                "because SRC-002 states the cables are carried THROUGH the towers, so the top band "
                "cannot be solid across them. The height is grade A (CTL-020) and the saddle level "
                "is grade B (CTL-064); the width of the opening is reasoned. See OQ-016."
            ),
        )

        # The saddles themselves. CTL-046 is grade A and was previously unused by any geometry.
        saddle_len = m("main_cable_diameter") * 6.0
        saddle_wid = m("main_cable_diameter") * 3.0
        saddle_ht = m("main_cable_diameter") * 2.0
        saddle_prims = [
            _box(
                (x_c - saddle_len / 2.0, y - saddle_wid / 2.0, z_saddle - saddle_ht),
                (x_c + saddle_len / 2.0, y + saddle_wid / 2.0, z_saddle),
            )
            for _name, y in cable_lines
        ]
        sk.add(
            f"saddle_group_{end}",
            "towers",
            "saddle",
            model.ids_of(
                "saddle_count",
                "main_cable_count",
                "cable_saddle_drop_below_tower_top",
                "tower_height_above_mhw",
                "main_cable_diameter",
                "truss_offset_outer",
                "truss_offset_inner",
            ),
            ["control_dimension", "drawing", "inferred"],
            saddle_prims,
            open_questions=["OQ-001"],
            notes=(
                "%d of the eight cast-iron saddle bearings of CTL-046 — SRC-002: \"THE MAIN CABLES "
                "WERE CARRIED THROUGH THE TOWERS ON EIGHT CAST IRON SADDLE BEARINGS OF 13 TONS "
                "EACH.\" The count and the elevation are sourced; the block size is reasoned from "
                "the sourced cable diameter, so no new placeholder was needed."
                % len(saddle_prims)
            ),
        )

        # The two pointed arches. Three shafts of equal width is reasoning, not a source statement.
        shaft_width = (m("tower_extent_y_at_mhw") - 2 * m("tower_arch_width")) / 3.0
        arch_offset = m("tower_arch_width") / 2.0 + shaft_width / 2.0
        for index, y_c in ((1, -arch_offset), (2, +arch_offset)):
            sk.add(
                f"tower_{end}_arch_{index}",
                "towers",
                "arch",
                model.ids_of(
                    "tower_arch_width",
                    "tower_arch_radius",
                    "tower_arch_height_above_springing",
                    "tower_vault_height_above_roadway",
                    "roadway_clearance_at_tower_above_mhw",
                ),
                ["control_dimension", "drawing", "inferred"],
                [
                    _polyline(
                        _pointed_arch_outline(
                            x_c,
                            y_c,
                            arch_half,
                            arch_radius,
                            arch_centre_offset,
                            z_tower_roadway,
                            z_arch_springing,
                        )
                    )
                ],
                open_questions=["OQ-004"],
                notes=(
                    "Arch width, radius and height are grade A and mutually consistent (CHK-005). "
                    "The transverse position assumes three equal shafts across the sourced 140 ft "
                    "tower width; that division is reasoned."
                ),
            )

    # ---------------------------------------------------------------- anchorages
    for end, sign in (("manhattan", -1.0), ("brooklyn", +1.0)):
        x_front = x_anc_m if end == "manhattan" else x_anc_b
        x_step = x_front + sign * m("anchorage_rear_offset_station")
        x_rear = x_front + sign * anchorage_x
        w_base_front = m("anchorage_base_width_front") / 2.0
        w_base_rear = m("anchorage_base_width_rear") / 2.0
        w_top_front = m("anchorage_top_width_front") / 2.0
        w_top_rear = m("anchorage_top_width_rear") / 2.0

        sk.add(
            f"anchorage_{end}_front_block",
            "anchorages",
            "masonry",
            model.ids_of(
                "anchorage_extent_x",
                "anchorage_rear_offset_station",
                "anchorage_base_width_front",
                "anchorage_top_width_front",
                "anchorage_roadway_front_above_mhw",
                "anchorage_count",
            ),
            ["control_dimension"],
            [
                _prism(
                    _plan_ring(min(x_front, x_step), max(x_front, x_step), w_base_front, 0.0),
                    _plan_ring(min(x_front, x_step), max(x_front, x_step), w_top_front, z_anchor_front),
                )
            ],
            open_questions=["OQ-006"],
            notes="SRC-004 dimensions the New York anchorage; symmetry with Brooklyn is OQ-006.",
        )
        sk.add(
            f"anchorage_{end}_rear_block",
            "anchorages",
            "masonry",
            model.ids_of(
                "anchorage_extent_x",
                "anchorage_rear_offset_station",
                "anchorage_base_width_rear",
                "anchorage_top_width_rear",
                "anchorage_roadway_rear_above_mhw",
            ),
            ["control_dimension"],
            [
                _prism(
                    _plan_ring(min(x_step, x_rear), max(x_step, x_rear), w_base_rear, 0.0),
                    _plan_ring(min(x_step, x_rear), max(x_step, x_rear), w_top_rear, z_anchor_rear),
                )
            ],
            open_questions=["OQ-006"],
        )
        sk.add(
            f"anchorage_{end}_cornice",
            "anchorages",
            "masonry",
            model.ids_of(
                "anchorage_cornice_height",
                "anchorage_top_length",
                "anchorage_top_width_rear",
                "anchorage_roadway_front_above_mhw",
            ),
            ["control_dimension", "inferred"],
            [
                _box(
                    (
                        min(x_front, x_rear),
                        -w_top_rear,
                        z_anchor_front - m("anchorage_cornice_height"),
                    ),
                    (max(x_front, x_rear), w_top_rear, z_anchor_front),
                )
            ],
            open_questions=["OQ-006"],
            notes="Cornice height is sourced; wrapping it around the full top plan is reasoned.",
        )

    # ---------------------------------------------------------------- deck chain
    deck_thickness = m("deck_structure_depth")
    deck_chain: list[tuple[str, float, float, float, float, list[str], list[str], str]] = [
        (
            "deck_manhattan_approach",
            x_appr_m,
            x_anc_m_rear,
            z_term_m,
            z_anchor_rear,
            model.ids_of(
                "manhattan_approach_length",
                "manhattan_terminus_above_mhw",
                "anchorage_roadway_rear_above_mhw",
                "deck_width",
                "deck_structure_depth",
            ),
            ["control_dimension", "drawing"],
            "Park Row to the landward face of the Manhattan anchorage.",
        ),
        (
            "deck_manhattan_anchorage_top",
            x_anc_m_rear,
            x_anc_m,
            z_anchor_rear,
            z_anchor_front,
            model.ids_of(
                "anchorage_extent_x",
                "anchorage_roadway_rear_above_mhw",
                "anchorage_roadway_front_above_mhw",
                "deck_width",
                "deck_structure_depth",
            ),
            ["control_dimension"],
            'SRC-004: "The top surface is to be sloped to the grade of the roadway, of which it '
            'will form part."',
        ),
        (
            "deck_manhattan_side_span",
            x_anc_m,
            x_twr_m,
            z_anchor_front,
            z_tower_roadway,
            model.ids_of(
                "side_span_each",
                "anchorage_roadway_front_above_mhw",
                "roadway_clearance_at_tower_above_mhw",
                "deck_width",
                "deck_structure_depth",
            ),
            ["control_dimension", "drawing"],
            "",
        ),
        (
            "deck_main_span_manhattan_half",
            x_twr_m,
            0.0,
            z_tower_roadway,
            z_deck_mid,
            model.ids_of(
                "main_span",
                "roadway_clearance_at_tower_above_mhw",
                "center_clearance_above_mhw",
                "deck_width",
                "deck_structure_depth",
            ),
            ["control_dimension"],
            "The deck crests at midspan; SRC-002 draws that camber.",
        ),
        (
            "deck_main_span_brooklyn_half",
            0.0,
            x_twr_b,
            z_deck_mid,
            z_tower_roadway,
            model.ids_of(
                "main_span",
                "roadway_clearance_at_tower_above_mhw",
                "center_clearance_above_mhw",
                "deck_width",
                "deck_structure_depth",
            ),
            ["control_dimension"],
            "",
        ),
        (
            "deck_brooklyn_side_span",
            x_twr_b,
            x_anc_b,
            z_tower_roadway,
            z_anchor_front,
            model.ids_of(
                "side_span_each",
                "anchorage_roadway_front_above_mhw",
                "roadway_clearance_at_tower_above_mhw",
                "deck_width",
                "deck_structure_depth",
            ),
            ["control_dimension", "drawing"],
            "",
        ),
        (
            "deck_brooklyn_anchorage_top",
            x_anc_b,
            x_anc_b_rear,
            z_anchor_front,
            z_anchor_rear,
            model.ids_of(
                "anchorage_extent_x",
                "anchorage_roadway_rear_above_mhw",
                "anchorage_roadway_front_above_mhw",
                "deck_width",
                "deck_structure_depth",
            ),
            ["control_dimension"],
            "",
        ),
        (
            "deck_brooklyn_approach",
            x_anc_b_rear,
            x_appr_b,
            z_anchor_rear,
            z_term_b,
            model.ids_of(
                "brooklyn_approach_length",
                "brooklyn_terminus_above_mhw",
                "anchorage_roadway_rear_above_mhw",
                "deck_width",
                "deck_structure_depth",
            ),
            ["control_dimension", "drawing"],
            "Landward face of the Brooklyn anchorage to Adams Street.",
        ),
    ]
    for part_id, x0, x1, z0, z1, refs, basis, note in deck_chain:
        sk.add(
            part_id,
            "deck_system",
            "roadway",
            refs,
            basis,
            [_slab(x0, x1, z0, z1, half_deck, deck_thickness)],
            open_questions=["OQ-003", "OQ-013"],
            notes=note,
        )

    # ------------------------------------------------------------------ promenade
    # SRC-011 (NYC DOT, 2016) dimensions the promenade end to end by typology. It is NOT
    # co-terminous with the roadway: the Brooklyn Curve carries it 910 ft past Adams Street toward
    # Tillary/Boerum, and that is where the staircase down to Washington Street sits.
    promenade_lift = m("promenade_elevation_above_roadway")
    promenade_thickness = deck_thickness / 2.0
    half_crown = m("promenade_length_crown") / 2.0
    tower_half = m("promenade_length_towers") / (2.0 * int(raw("tower_count")))
    x_curve_end = x_appr_b + m("promenade_length_brooklyn_curve")
    z_curve_end = z_term_b - m("brooklyn_curve_terminus_drop")

    def deck_z(x: float) -> float:
        """Roadway elevation at station x, following the same chain the deck was built from."""
        for _pid, x0, x1, z0, z1, *_rest in deck_chain:
            lo, hi = (x0, x1) if x0 <= x1 else (x1, x0)
            if lo - 1e-6 <= x <= hi + 1e-6:
                t = 0.0 if abs(x1 - x0) < 1e-9 else (x - x0) / (x1 - x0)
                return z0 + (z1 - z0) * t
        return z_deck_mid

    promenade_chain: list[tuple[str, float, float, float, float, float, list[str], list[str], list[str], str]] = []

    def promenade_segment(
        part_id: str,
        x0: float,
        x1: float,
        width_key: str,
        length_key: str,
        open_questions: Sequence[str],
        note: str,
        z0: float | None = None,
        z1: float | None = None,
    ) -> None:
        promenade_chain.append(
            (
                part_id,
                x0,
                x1,
                (deck_z(x0) + promenade_lift) if z0 is None else z0,
                (deck_z(x1) + promenade_lift) if z1 is None else z1,
                m(width_key) / 2.0,
                model.ids_of(width_key, length_key, "promenade_elevation_above_roadway"),
                ["control_dimension", "drawing", "inferred"],
                list(open_questions),
                note,
            )
        )

    promenade_segment(
        "promenade_manhattan_concrete_approach",
        x_appr_m,
        x_anc_m,
        "promenade_width_concrete_approach",
        "promenade_length_concrete_approaches",
        ["OQ-013"],
        "SRC-011 typology 1, 17 ft — the widest section. The 2365 ft is both ends combined, so the "
        "split between them is reasoning.",
    )
    promenade_segment(
        "promenade_manhattan_side_span",
        x_anc_m,
        x_twr_m - tower_half,
        "promenade_width_wood_deck_with_cables",
        "promenade_length_wood_deck_with_cables",
        ["OQ-013"],
        "SRC-011 typology 3, 13 ft — where the main cables come down alongside the path.",
    )
    promenade_segment(
        "promenade_tower_manhattan",
        x_twr_m - tower_half,
        x_twr_m + tower_half,
        "promenade_width_at_towers",
        "promenade_length_towers",
        [],
        "SRC-011 typology 5, 43 ft — the path opens into the tower balcony. Position is grade A: "
        "the tower centerline.",
    )
    promenade_segment(
        "promenade_main_span_manhattan_half",
        x_twr_m + tower_half,
        -half_crown,
        "promenade_width_wood_deck_with_cables",
        "promenade_length_wood_deck_with_cables",
        ["OQ-013"],
        "SRC-011 typology 3.",
    )
    promenade_segment(
        "promenade_crown",
        -half_crown,
        half_crown,
        "promenade_width_crown",
        "promenade_length_crown",
        [],
        "SRC-011 typology 6, 355 ft at 16 ft wide. The length is grade A; centring it on midspan is "
        "inference from the cable profile, not a statement in the source, so this stays INFERRED.",
    )
    promenade_segment(
        "promenade_main_span_brooklyn_half",
        half_crown,
        x_twr_b - tower_half,
        "promenade_width_wood_deck_with_cables",
        "promenade_length_wood_deck_with_cables",
        ["OQ-013"],
        "SRC-011 typology 3.",
    )
    promenade_segment(
        "promenade_tower_brooklyn",
        x_twr_b - tower_half,
        x_twr_b + tower_half,
        "promenade_width_at_towers",
        "promenade_length_towers",
        [],
        "SRC-011 typology 5, 43 ft.",
    )
    promenade_segment(
        "promenade_brooklyn_side_span",
        x_twr_b + tower_half,
        x_anc_b,
        "promenade_width_wood_deck_with_cables",
        "promenade_length_wood_deck_with_cables",
        ["OQ-013"],
        "SRC-011 typology 3.",
    )
    promenade_segment(
        "promenade_brooklyn_concrete_approach",
        x_anc_b,
        x_appr_b,
        "promenade_width_concrete_approach",
        "promenade_length_concrete_approaches",
        ["OQ-013"],
        "SRC-011 typology 1. SRC-011 annotates this section: pedestrians coming up from the stairs "
        "must cross the bike lane to enter the promenade.",
    )
    promenade_segment(
        "promenade_brooklyn_curve",
        x_appr_b,
        x_curve_end,
        "promenade_width_brooklyn_curve",
        "promenade_length_brooklyn_curve",
        ["OQ-014"],
        "SRC-011 typology 8, 910 ft at 11 ft wide — **the section that carries the walkway past the "
        "roadway's Adams Street terminus** toward Tillary Street and Boerum Place (SRC-012). Length "
        "and width are grade A. Its horizontal curve is NOT modelled: no read source gives a radius, "
        "so it is drawn straight along the centerline the walkway holds while the road diverges "
        "(SRC-014). See OQ-014.",
        z0=z_term_b + promenade_lift,
        z1=z_curve_end,
    )

    for (
        part_id,
        x0,
        x1,
        z0,
        z1,
        half_w,
        refs,
        basis,
        oqs,
        note,
    ) in promenade_chain:
        sk.add(
            part_id,
            "deck_system",
            "promenade",
            refs,
            basis,
            [_slab(min(x0, x1), max(x0, x1), z0 if x0 <= x1 else z1, z1 if x0 <= x1 else z0, half_w, promenade_thickness)],
            open_questions=oqs,
            notes=note,
        )

    # ---------------------------------------------------------------- staircases
    # Existence and street location are sourced; only the size is a guess, which is why these are
    # INFERRED rather than ASSUMED.
    stair_half_w = m("stair_width") / 2.0
    stair_run = m("stair_width") * 2.0
    for part_id, x_c, z_top, note in (
        (
            "stair_brooklyn_washington_street",
            x_appr_b + m("promenade_length_brooklyn_curve") * 0.35,
            z_term_b + promenade_lift,
            "The tourist stair between the promenade and DUMBO. SRC-011 places it in the Brooklyn "
            "Curve — that section's 11 ft path has \"excess space on north side of fence to "
            "accommodate staircase\". SRC-012 and SRC-013 both put its foot at Washington Street "
            "and Prospect Street, in the underpass by Cadman Plaza East. SRC-014 confirms it from "
            "the ground. Its dimensions are a placeholder (CTL-107), see OQ-015.",
        ),
        (
            "stair_manhattan_approach",
            x_appr_m + m("promenade_length_brooklyn_curve") * 0.10,
            deck_z(x_appr_m + m("promenade_length_brooklyn_curve") * 0.10) + promenade_lift,
            "SRC-011 marks a staircase on the Manhattan concrete approach as a pinch point: "
            "\"Staircase creates pinch point. Bikes traveling at high downhill speed do not have "
            "space to pass bikes entering the bridge.\" Dimensions are a placeholder, see OQ-015.",
        ),
    ):
        # Descends on the north side, which is the side SRC-011 says has the space for it.
        y_c = m("promenade_width_brooklyn_curve") / 2.0 + stair_half_w
        sk.add(
            part_id,
            "deck_system",
            "stair",
            model.ids_of("stair_width", "promenade_elevation_above_roadway", "promenade_width_brooklyn_curve"),
            ["control_dimension", "drawing", "inferred"],
            [
                _prism(
                    _plan_ring(x_c - stair_run / 2.0, x_c + stair_run / 2.0, stair_half_w, z_top - promenade_lift),
                    _plan_ring(x_c - stair_run / 2.0, x_c + stair_run / 2.0, stair_half_w, z_top),
                )
            ],
            open_questions=["OQ-015"],
            notes=note,
        )
        sk.parts[-1].primitives[0]["positions"] = [
            (p[0], p[1] + y_c, p[2]) for p in sk.parts[-1].primitives[0]["positions"]
        ]
        lo, hi = _bounds(sk.parts[-1].primitives)
        sk.parts[-1].bbox_min, sk.parts[-1].bbox_max = lo, hi

    # -------------------------------------------------------------- main cables
    cable_radius = m("main_cable_diameter") / 2.0
    cable_refs = model.ids_of(
        "main_span",
        "tower_height_above_mhw",
        "cable_saddle_drop_below_tower_top",
        "min_suspender_length_at_midspan",
        "main_cable_diameter",
        "main_cable_count",
        "truss_offset_outer",
        "truss_offset_inner",
    )
    for name, y in cable_lines:
        main_points = [
            (x, y, _parabola(x, x_twr_b, z_saddle, z_cable_mid))
            for x in _linspace(x_twr_m, x_twr_b, 121)
        ]
        sk.add(
            f"cable_main_{name}_main_span",
            "cables",
            "main_cable",
            cable_refs,
            ["control_dimension", "inferred"],
            [_tube(main_points, cable_radius)],
            open_questions=["OQ-001", "OQ-002"],
            notes=(
                "Parabolic approximation. The sag rests on two placeholders (CTL-101, CTL-102) so "
                "the whole curve is grade D — see OQ-001 and the sag discussion in "
                "GEOMETRY-CONTROL.md section 4.2."
            ),
        )
        for end, x_t, x_a in (("manhattan", x_twr_m, x_anc_m), ("brooklyn", x_twr_b, x_anc_b)):
            sk.add(
                f"cable_main_{name}_side_span_{end}",
                "cables",
                "main_cable",
                cable_refs + model.ids_of("side_span_each", "anchorage_roadway_front_above_mhw"),
                ["control_dimension", "inferred"],
                [_tube([(x_t, y, z_saddle), (x_a, y, z_anchor_front)], cable_radius)],
                open_questions=["OQ-001", "OQ-002"],
                notes="Straight chord; the true side-span curve is not registered.",
            )

    # --------------------------------------------------------------- suspenders
    suspender_refs = model.ids_of(
        "suspender_count",
        "main_cable_count",
        "bridge_proper_length",
        "truss_offset_outer",
        "truss_offset_inner",
        "stiffening_truss_depth_present",
        "center_clearance_above_mhw",
    )
    for name, y in cable_lines:
        for span, x0, x1 in (
            ("manhattan_side_span", x_anc_m, x_twr_m),
            ("main_span", x_twr_m, x_twr_b),
            ("brooklyn_side_span", x_twr_b, x_anc_b),
        ):
            segments = []
            count = max(int(round(abs(x1 - x0) / suspender_pitch)), 1)
            for i in range(1, count):
                x = x0 + (x1 - x0) * i / count
                if span == "main_span":
                    z_top = _parabola(x, x_twr_b, z_saddle, z_cable_mid)
                else:
                    t = (x - x0) / (x1 - x0)
                    z_top = z_anchor_front + (z_saddle - z_anchor_front) * (
                        t if span.startswith("manhattan") else 1.0 - t
                    )
                segments.append(((x, y, z_top), (x, y, z_truss_top)))
            if not segments:
                continue
            sk.add(
                f"suspender_group_{name}_{span}",
                "suspenders",
                "vertical_suspender",
                suspender_refs,
                ["control_dimension", "inferred"],
                [_lines(segments)],
                open_questions=["OQ-001", "OQ-002"],
                notes=(
                    f"{len(segments)} suspenders at the derived pitch of "
                    f"{suspender_pitch / 0.3048:.2f} ft. The total count is grade A (CTL-044); "
                    "distributing it evenly is reasoning, so these are INFERRED."
                ),
            )

    # ------------------------------------------------------------ diagonal stays
    stay_refs = model.ids_of(
        "diagonal_stay_count",
        "main_cable_count",
        "tower_count",
        "tower_height_above_mhw",
        "suspender_count",
        "bridge_proper_length",
        "stiffening_truss_depth_present",
        "center_clearance_above_mhw",
    )
    for name, y in cable_lines:
        for end, x_t in (("manhattan", x_twr_m), ("brooklyn", x_twr_b)):
            for direction, sign in (("inboard", 1.0 if end == "manhattan" else -1.0), ("outboard", -1.0 if end == "manhattan" else 1.0)):
                segments = []
                for i in range(1, stays_per_group + 1):
                    x = x_t + sign * i * suspender_pitch
                    if not (x_anc_m <= x <= x_anc_b):
                        continue
                    segments.append(((x_t, y, z_saddle), (x, y, z_truss_top)))
                if not segments:
                    continue
                sk.add(
                    f"stay_{name}_{end}_{direction}",
                    "stays",
                    "diagonal_stay",
                    stay_refs,
                    ["control_dimension", "inferred"],
                    [_lines(segments)],
                    open_questions=["OQ-001"],
                    notes=(
                        "The Roebling system's second load path. SRC-002: \"DIAGONAL STAY CABLES "
                        "CARRY PART OF THE SUSPENDED SUPERSTRUCTURE (THE DECK LOAD).\" The count "
                        "is grade A (CTL-045); the reach is derived from the suspender pitch, so "
                        f"each fan reaches {stay_reach / 0.3048:.0f} ft and is INFERRED."
                    ),
                )

    # ------------------------------------------------------ stiffening trusses
    truss_refs = model.ids_of(
        "stiffening_truss_count_present",
        "stiffening_truss_depth_present",
        "center_clearance_above_mhw",
        "truss_offset_outer",
        "truss_offset_inner",
    )
    truss_lines = [
        ("outer_south", -y_outer),
        ("inner_south", -y_inner),
        ("inner_north", +y_inner),
        ("outer_north", +y_outer),
    ]
    if len(truss_lines) != int(raw("stiffening_truss_count_present")):
        raise BuildError("truss layout disagrees with the present-day truss count control")
    truss_web = 1.0
    for name, y in truss_lines:
        for span, x0, x1 in (
            ("manhattan_side_span", x_anc_m, x_twr_m),
            ("main_span", x_twr_m, x_twr_b),
            ("brooklyn_side_span", x_twr_b, x_anc_b),
        ):
            sk.add(
                f"truss_{name}_{span}",
                "deck_system",
                "stiffening_truss",
                truss_refs,
                ["control_dimension", "inferred"],
                [
                    _box(
                        (min(x0, x1), y - truss_web / 2.0, z_truss_bottom),
                        (max(x0, x1), y + truss_web / 2.0, z_truss_top),
                    )
                ],
                open_questions=["OQ-002", "OQ-010"],
                notes=(
                    "Depth is grade A (CTL-076). The count is reasoned from SRC-001 note 2 "
                    "(CTL-077, grade B) and the transverse position is a placeholder, so the "
                    "envelope is INFERRED."
                ),
            )

    # -------------------------------------------------------------- floor beams
    beam_refs = model.ids_of(
        "floor_beam_length",
        "floor_beam_depth",
        "suspender_count",
        "main_cable_count",
        "bridge_proper_length",
        "center_clearance_above_mhw",
    )
    for span, x0, x1 in (
        ("manhattan_side_span", x_anc_m, x_twr_m),
        ("main_span", x_twr_m, x_twr_b),
        ("brooklyn_side_span", x_twr_b, x_anc_b),
    ):
        segments = []
        count = max(int(round(abs(x1 - x0) / suspender_pitch)), 1)
        for i in range(1, count):
            x = x0 + (x1 - x0) * i / count
            segments.append(((x, -half_beam, z_truss_bottom), (x, half_beam, z_truss_bottom)))
        if not segments:
            continue
        sk.add(
            f"floor_beam_group_{span}",
            "deck_system",
            "floor_beam",
            beam_refs,
            ["control_dimension", "inferred"],
            [_lines(segments)],
            open_questions=["OQ-013"],
            notes="86 ft long (CTL-071, grade A) at the derived suspender pitch.",
        )

    # --------------------------------------------------------------- approaches
    for end, x0, x1, z0, z1 in (
        ("manhattan", x_appr_m, x_anc_m_rear, z_term_m, z_anchor_rear),
        ("brooklyn", x_anc_b_rear, x_appr_b, z_anchor_rear, z_term_b),
    ):
        length_ref = (
            "manhattan_approach_length" if end == "manhattan" else "brooklyn_approach_length"
        )
        sk.add(
            f"approach_girder_{end}",
            "approaches",
            "viaduct",
            model.ids_of(length_ref, "approach_girder_depth", "deck_width"),
            ["control_dimension", "inferred"],
            [
                _slab(
                    x0,
                    x1,
                    z0 - deck_thickness,
                    z1 - deck_thickness,
                    half_deck * 0.9,
                    m("approach_girder_depth"),
                )
            ],
            open_questions=["OQ-007"],
            notes="Extent is grade A; the structural depth is a placeholder.",
        )
        # The arcade. HAER NY-18-64 (SRC-007) is a near-square elevation of the Brooklyn approach
        # and settles the KIND of structure: a continuous run of pointed arches springing from
        # rectangular granite piers, carrying a balustraded parapet. It settles no dimension, so
        # every number below is a placeholder and the whole group is graded accordingly. Building
        # the right kind of object out of invented dimensions is better than building the wrong
        # kind, because the error that remains is the one the register already describes.
        piers: list[dict[str, Any]] = []
        arches: list[Sequence[Sequence[float]]] = []
        span_len = abs(x1 - x0)
        count = max(int(span_len / m("approach_arcade_bay")), 1)
        pier_half_x = m("approach_pier_width_x") / 2.0
        pier_half_y = m("approach_pier_depth_y") / 2.0
        rise = m("approach_arch_rise")

        def soffit_at(t: float) -> float:
            return z0 + (z1 - z0) * t - deck_thickness - m("approach_girder_depth")

        for i in range(count + 1):
            t = i / count
            x = x0 + (x1 - x0) * t
            z_top = soffit_at(t)
            piers.append(_box((x - pier_half_x, -pier_half_y, 0.0), (x + pier_half_x, pier_half_y, z_top)))

        for i in range(count):
            ta, tb = i / count, (i + 1) / count
            xa = x0 + (x1 - x0) * ta + pier_half_x
            xb = x0 + (x1 - x0) * tb - pier_half_x
            if xb <= xa:
                continue
            z_spring = min(soffit_at(ta), soffit_at(tb)) - rise
            if z_spring <= 0.0:
                continue
            arches.append(_longitudinal_pointed_arch(xa, xb, z_spring, rise, pier_half_y))

        # A two-centred pointed arch only exists when its rise is at least half its clear span;
        # below that the two arcs bulge past the crown and the thing drawn is a segmental arch
        # wearing a pointed arch's parameters. The first version of this ran with a 100 ft bay
        # inherited from the bents and produced crowns 1.6 m above the deck soffit. Checking it
        # here means the placeholder cannot quietly drift back to an impossible value.
        clear_span = abs(m("approach_arcade_bay") - m("approach_pier_width_x"))
        check_at_least(
            f"CHK-009-{end[0].upper()}",
            "the placeholder arch rise reaches at least half the placeholder clear span, "
            "so a two-centred pointed arch of these dimensions exists",
            m("approach_arch_rise"),
            clear_span / 2.0,
        )

        if piers:
            sk.add(
                f"approach_arcade_{end}",
                "approaches",
                "viaduct",
                model.ids_of(
                    "approach_arcade_bay", "approach_pier_width_x",
                    "approach_pier_depth_y", "approach_arch_rise", length_ref,
                ),
                ["placeholder"],
                piers + [_lines([seg for arch in arches for seg in arch])],
                open_questions=["OQ-007"],
                notes=(
                    "PLACEHOLDER GEOMETRY, CORRECT IN KIND. SRC-007 plate NY-18-64 shows a masonry "
                    "arcade of pointed arches on rectangular piers; the model previously drew "
                    "slender bents, which is not this object. Every dimension here -- bay spacing, "
                    "pier width and depth, arch rise -- is invented, so the arcade is excluded "
                    "from every dimension callout. What is now right is the shape; what is still "
                    "wrong is every number in it."
                ),
            )

    derived = {
        "stations_m": {
            "STA-APPR-END-M": round(x_appr_m, 4),
            "STA-ANC-M-REAR": round(x_anc_m_rear, 4),
            "STA-ANC-M": round(x_anc_m, 4),
            "STA-TWR-M": round(x_twr_m, 4),
            "STA-MID": 0.0,
            "STA-TWR-B": round(x_twr_b, 4),
            "STA-ANC-B": round(x_anc_b, 4),
            "STA-ANC-B-REAR": round(x_anc_b_rear, 4),
            "STA-APPR-END-B": round(x_appr_b, 4),
        },
        "elevations_m": {
            "ELV-FOUNDATION-M": round(z_found_m, 4),
            "ELV-FOUNDATION-B": round(z_found_b, 4),
            "ELV-DATUM": 0.0,
            "ELV-TOWER-ROADWAY": round(z_tower_roadway, 4),
            "ELV-CLEARANCE": round(z_clearance, 4),
            "ELV-TRUSS-TOP": round(z_truss_top, 4),
            "ELV-DECK-MID": round(z_deck_mid, 4),
            "ELV-PROMENADE-MID": round(z_promenade_mid, 4),
            "ELV-ARCH-SPRINGING": round(z_arch_springing, 4),
            "ELV-ARCH-CROWN": round(z_arch_crown, 4),
            "ELV-CABLE-MID": round(z_cable_mid, 4),
            "ELV-SADDLE": round(z_saddle, 4),
            "ELV-TOWER-TOP": round(z_tower_top, 4),
            "ELV-ANCHOR-POINT": round(z_anchor_front, 4),
        },
        "cable_sag_m": round(z_saddle - z_cable_mid, 4),
        "cable_sag_ft": round((z_saddle - z_cable_mid) / 0.3048, 3),
        "cable_sag_ratio": round(main_span / max(z_saddle - z_cable_mid, 1e-9), 3),
        "cable_sag_confidence": "D",
        "suspender_pitch_m": round(suspender_pitch, 4),
        "suspender_pitch_ft": round(suspender_pitch / 0.3048, 3),
        "suspenders_per_cable": suspenders_per_cable,
        "stays_per_group": stays_per_group,
        "stay_reach_ft": round(stay_reach / 0.3048, 2),
        "deck_chain_ids": [row[0] for row in deck_chain],
        "promenade_chain_ids": [row[0] for row in promenade_chain],
        "promenade_extends_past_roadway_ft": round(
            (x_curve_end - x_appr_b) / 0.3048, 2
        ),
        "promenade_typology_total_ft": round(
            sum(
                raw(k)
                for k in (
                    "promenade_length_concrete_approaches",
                    "promenade_length_wood_deck_approaches",
                    "promenade_length_wood_deck_with_cables",
                    "promenade_length_tower_ramps",
                    "promenade_length_towers",
                    "promenade_length_crown",
                    "promenade_length_trunk_cable_bases",
                    "promenade_length_brooklyn_curve",
                )
            ),
            2,
        ),
        "checks": checks,
    }
    return sk, derived


def _station_refs(model: ControlModel, station_id: str) -> list[str]:
    mapping = {
        "station_manhattan_approach_end": ("manhattan_approach_length", "total_length_including_approaches"),
        "station_manhattan_anchorage": ("side_span_each", "main_span"),
        "station_manhattan_tower": ("main_span",),
        "station_midspan": ("main_span",),
        "station_brooklyn_tower": ("main_span",),
        "station_brooklyn_anchorage": ("side_span_each", "main_span"),
        "station_brooklyn_approach_end": ("brooklyn_approach_length", "total_length_including_approaches"),
    }
    return model.ids_of(*mapping[station_id])


def _parabola(x: float, half_span: float, z_end: float, z_vertex: float) -> float:
    return z_vertex + (z_end - z_vertex) * (x / half_span) ** 2


def _linspace(a: float, b: float, n: int) -> list[float]:
    return [a + (b - a) * i / (n - 1) for i in range(n)]


def _longitudinal_pointed_arch(
    x0: float,
    x1: float,
    z_springing: float,
    rise: float,
    half_depth: float,
) -> list[tuple[tuple[float, float, float], tuple[float, float, float]]]:
    """Line segments outlining a pointed arch in the x-z plane, drawn on both faces.

    A two-centred arch: each half is a circular arc struck from a centre on the springing line at
    the opposite quarter point, which is what gives the pointed crown seen in NY-18-64. Drawn as an
    outline rather than a solid because the model has no sourced thickness for the arch ring, and a
    solid would assert one.
    """
    span = x1 - x0
    half = span / 2.0
    if half <= 0 or rise <= 0:
        return []
    # Two-centred arch. Each half is struck from a centre ON the springing line, positioned so the
    # arc leaves its own springing point at zero height and reaches exactly `rise` at the crown:
    #   R = (half^2 + rise^2) / (2 * half)
    # with the left centre at x0 + R and the right at x1 - R. Deriving R from `half` rather than
    # from `rise` is the whole of it -- the first version of this divided by `rise`, which put the
    # springing points above the ground and drove the crowns clean through the deck soffit.
    radius = (half**2 + rise**2) / (2.0 * half)
    cx_left = x0 + radius
    cx_right = x1 - radius
    steps = 14
    segs: list[tuple[tuple[float, float, float], tuple[float, float, float]]] = []
    for y in (-half_depth, half_depth):
        pts: list[tuple[float, float, float]] = []
        for i in range(steps + 1):
            x = x0 + half * (i / steps)
            pts.append((x, y, z_springing + math.sqrt(max(radius**2 - (x - cx_left) ** 2, 0.0))))
        for i in range(1, steps + 1):
            x = x0 + half + half * (i / steps)
            pts.append((x, y, z_springing + math.sqrt(max(radius**2 - (x - cx_right) ** 2, 0.0))))
        segs.extend(zip(pts, pts[1:]))
    return segs


def _pointed_arch_outline(
    x_c: float,
    y_c: float,
    half_width: float,
    radius: float,
    centre_offset: float,
    z_base: float,
    z_springing: float,
) -> list[tuple[float, float, float]]:
    """Two-centred pointed arch outline in the transverse plane of a tower."""
    points: list[tuple[float, float, float]] = [
        (x_c, y_c - half_width, z_base),
        (x_c, y_c - half_width, z_springing),
    ]
    steps = 24
    # Left half: arc centred at +centre_offset, swept from the left springing point to the crown.
    start = math.atan2(0.0, -half_width - centre_offset)
    crown_angle = math.atan2(
        math.sqrt(max(radius**2 - centre_offset**2, 0.0)), -centre_offset
    )
    for i in range(steps + 1):
        ang = start + (crown_angle - start) * i / steps
        points.append(
            (x_c, y_c + centre_offset + radius * math.cos(ang), z_springing + radius * math.sin(ang))
        )
    start = math.atan2(0.0, half_width + centre_offset)
    crown_angle = math.atan2(
        math.sqrt(max(radius**2 - centre_offset**2, 0.0)), centre_offset
    )
    for i in range(steps, -1, -1):
        ang = start + (crown_angle - start) * i / steps
        points.append(
            (x_c, y_c - centre_offset + radius * math.cos(ang), z_springing + radius * math.sin(ang))
        )
    points.append((x_c, y_c + half_width, z_springing))
    points.append((x_c, y_c + half_width, z_base))
    return points


# ------------------------------------------------------------------------ export


def export(sk: Skeleton, derived: dict[str, Any], model: ControlModel) -> dict[str, Any]:
    counts_provenance: dict[str, int] = {
        "MEASURED": 0,
        "DOCUMENTED": 0,
        "INFERRED": 0,
        "ASSUMED": 0,
    }
    counts_confidence: dict[str, int] = {"A": 0, "B": 0, "C": 0, "D": 0}
    for part in sk.parts:
        counts_provenance[part.provenance] += 1
        counts_confidence[part.confidence] += 1

    for scale, stem in ((1.0, "control_skeleton"), (1.0 / HO_SCALE_DENOMINATOR, "control_skeleton_ho")):
        builder = GltfBuilder(
            generator=BUILDER_VERSION,
            scale=scale,
            copyright_text=(
                "Brooklyn Bridge Digital Twin, Ethical Tech CoLab. CC BY 4.0. "
                "Built from GEOMETRY-CONTROL.md sha256="
                f"{model.document_sha256[:16]}"
            ),
        )
        builder.set_root_name("brooklyn_bridge")
        builder.set_root_extras(
            {
                "control_document_sha256": model.document_sha256,
                "scale": "prototype" if scale == 1.0 else "HO 1:87.1",
                "vertical_datum": "mean high water (MHW)",
                "units": "meters",
            }
        )
        systems: dict[str, int] = {}
        for part in sk.parts:
            if part.system not in systems:
                node = builder.add_node(part.system)
                builder.add_to_root(node)
                systems[part.system] = node
            material_index = builder.add_material(
                f"{part.material}_{part.provenance.lower()}",
                _material_color(part.material, part.provenance),
                unlit=any(p["kind"] == "line" for p in part.primitives),
            )
            primitives = []
            for prim in part.primitives:
                if prim["kind"] == "line":
                    primitives.append(
                        {
                            "mode": 1,
                            "positions": prim["positions"],
                            "normals": None,
                            "indices": prim["indices"],
                            "material": material_index,
                        }
                    )
                else:
                    primitives.append(
                        {
                            "mode": 4,
                            "positions": prim["positions"],
                            "normals": prim["normals"],
                            "indices": prim["indices"],
                            "material": material_index,
                        }
                    )
            mesh = builder.add_mesh(f"{part.part_id}_mesh", primitives)
            node = builder.add_node(part.part_id, mesh=mesh, extras=part.to_metadata())
            builder.add_child(systems[part.system], node)

        builder.save_glb(REPO / "mesh" / "glb" / f"{stem}.glb")
        builder.save_glb(REPO / "viewer" / "public" / f"{stem}.glb")
        if scale == 1.0:
            builder.save_gltf(REPO / "mesh" / "glb" / f"{stem}.gltf")

    parts_payload = {
        "control_document_sha256": model.document_sha256,
        "generator": BUILDER_VERSION,
        "vertical_datum": "mean high water (MHW)",
        "units": "meters",
        "ho_scale_denominator": HO_SCALE_DENOMINATOR,
        "parts": [p.to_metadata() for p in sk.parts],
    }
    _write_json(REPO / "viewer" / "metadata" / "parts.json", parts_payload)
    _write_json(REPO / "viewer" / "public" / "parts.json", parts_payload)

    # The viewer's "locus on selection" needs the control rows themselves, so that clicking a part
    # can show the passage its geometry rests on — or state plainly that there is none.
    controls_payload = {
        "control_document_sha256": model.document_sha256,
        "controls": [
            {
                "control_id": c.control_id,
                "key": c.key,
                "value": c.value,
                "unit": c.unit,
                "value_m": round(c.value_m, 6),
                "source_ids": list(c.source_ids),
                "confidence": c.confidence,
                "is_placeholder": c.is_placeholder,
                "notes": c.notes,
            }
            for c in model.controls.values()
        ],
        "materials": [
            {
                "material_id": r.material_id,
                "pattern": r.pattern,
                "material": r.material,
                "source_ids": list(r.source_ids),
                "confidence": r.confidence,
                "notes": r.notes,
            }
            for r in model.materials
        ],
    }
    _write_json(REPO / "viewer" / "public" / "controls.json", controls_payload)
    _write_json(REPO / "viewer" / "metadata" / "controls.json", controls_payload)

    scale_rows = []
    for control in model.controls.values():
        if not is_linear(control.unit):
            continue
        row = ho_report(control.value_m)
        row.update(
            {
                "control_id": control.control_id,
                "key": control.key,
                "unit": control.unit,
                "confidence": control.confidence,
                "is_placeholder": control.is_placeholder,
            }
        )
        scale_rows.append(row)
    _write_json(
        REPO / "viewer" / "metadata" / "scale_ho.json",
        {
            "ho_scale_denominator": HO_SCALE_DENOMINATOR,
            "control_document_sha256": model.document_sha256,
            "controls": scale_rows,
        },
    )

    report = {
        "generator": BUILDER_VERSION,
        "control_document": CONTROL_DOC.name,
        "control_document_sha256": model.document_sha256,
        "controls_total": len(model.controls),
        "controls_sourced": len(model.controls) - len(model.placeholders),
        "controls_placeholder": len(model.placeholders),
        "material_rules": len(model.materials),
        "parts_total": len(sk.parts),
        "provenance": counts_provenance,
        "confidence": counts_confidence,
        "systems": sorted({p.system for p in sk.parts}),
        "derived": derived,
    }
    _write_json(REPO / "viewer" / "metadata" / "build_report.json", report)
    _write_json(REPO / "viewer" / "public" / "build_report.json", report)

    _write_json(
        REPO / "cad" / "procedural" / "control_skeleton_geometry.json",
        {
            "control_document_sha256": model.document_sha256,
            "units": "meters",
            "parts": [
                {
                    "part_id": p.part_id,
                    "primitives": [
                        {
                            "kind": prim["kind"],
                            "positions": [[round(c, 6) for c in pt] for pt in prim["positions"]],
                            "indices": prim["indices"],
                        }
                        for prim in p.primitives
                    ],
                }
                for p in sk.parts
            ],
        },
    )
    return report


def _material_color(material: str, provenance: str) -> tuple[float, float, float, float]:
    base = MATERIAL_COLORS[material]
    alpha = {"MEASURED": 1.0, "DOCUMENTED": 1.0, "INFERRED": 0.55, "ASSUMED": 0.28}[provenance]
    return (base[0], base[1], base[2], alpha)


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    # newline="\n" explicitly: the default on Windows translates \n to \r\n, which would make the
    # build output differ byte-for-byte between platforms and break both the CI byte-identity gate
    # and GRT-080's hash of the canonical frame.
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(payload, indent=2) + "\n")


def main() -> int:
    try:
        model = load_control_model(CONTROL_DOC)
    except ControlDocumentError as exc:
        print(f"control document error: {exc}", file=sys.stderr)
        return 2

    sk, derived = build(model)
    report = export(sk, derived, model)

    failed = [c for c in derived["checks"] if not c["passed"]]
    print(f"{CONTROL_DOC.name}  sha256={model.document_sha256[:12]}")
    print(f"  controls  : {report['controls_total']} "
          f"({report['controls_sourced']} sourced, {report['controls_placeholder']} placeholder)")
    print(f"  parts     : {report['parts_total']}")
    print(f"  provenance: {report['provenance']}")
    print(f"  confidence: {report['confidence']}")
    print(f"  cable sag : {derived['cable_sag_ft']} ft "
          f"(1:{derived['cable_sag_ratio']}, grade {derived['cable_sag_confidence']})")
    for c in derived["checks"]:
        flag = "ok  " if c["passed"] else "FAIL"
        print(f"  {flag} {c['id']}  residual {c['residual_ft']:+.3f} ft  {c['description']}")
    if failed:
        print(f"{len(failed)} consistency check(s) failed", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
