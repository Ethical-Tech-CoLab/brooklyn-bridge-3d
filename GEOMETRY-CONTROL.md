# Geometry Control

**This file is the source of truth for every dimensional value in this repository.**

`scripts/build_control_skeleton.py` *parses this file*. It carries no copy of any number. If a value
is not in a control table below, it does not exist in the model. To change the model, change this
file and rebuild — test `GRT-001` fails the build if the parts manifest was produced from a
different SHA-256 of this document.

Milestone 1 status: **66 sourced controls, 12 placeholders.** Every sourced row traces to one of the
five read sources in [SOURCE-REGISTER.md](SOURCE-REGISTER.md), two of which are period primaries and
one of which is the only measured drawing of any East River suspension bridge in the national record.

---

## 1. Coordinate system and datum

| Item | Definition |
|---|---|
| World units | meters |
| Origin | midpoint of the main span, on the bridge longitudinal centerline, at the vertical datum |
| Vertical datum | **mean high water (MHW), `z = 0`** |
| +X | along the bridge longitudinal axis, toward the **Brooklyn** end |
| −X | along the bridge longitudinal axis, toward the **Manhattan** end |
| +Y | across the bridge, toward the **north** side |
| +Z | vertical, up |
| Handedness | right-handed, Z-up (the glTF export converts to Y-up) |
| HO export scale | 1 : 87.1, see [SCALE-HO.md](SCALE-HO.md) |

**The vertical datum is declared, not converted.** SRC-002 labels its own baseline `MEAN HIGH WATER`
and SRC-004 measures everything "above high water"; authoring in MHW therefore keeps every elevation
in the unit its source used. The relationship between MHW and NAVD88 is **not registered**, so no
conversion to a geodetic vertical datum is performed anywhere in this repository. A consumer that
needs NAVD88 must supply the offset at placement time. See OQ-009.

**Manhattan-is-negative-X is a modelling convention, not a survey fact.** The real-world azimuth of
the bridge axis is not registered. See OQ-008.

---

## 2. Control dimensions

Machine-parsed. Column contract: `Control ID | Key | Value | Unit | Source IDs | Confidence | Notes`.
`Value` must be a bare decimal with no thousands separators. `Unit` is one of `ft`, `in`, `m`, `mm`,
`count`, `ratio`.

### 2.1 Longitudinal chain

| Control ID | Key | Value | Unit | Source IDs | Confidence | Notes |
|---|---|---:|---|---|---|---|
| CTL-001 | main_span | 1595.5 | ft | SRC-001, SRC-002, SRC-003 | A | Tower centerline to tower centerline. SRC-002 dimensions it `1595'-6" MAIN SPAN`; SRC-001 gives 1,595.5 ft; SRC-003 "the bridge's 1,595.5-foot span broke all world records for span length". |
| CTL-002 | side_span_each | 930 | ft | SRC-001, SRC-002, SRC-004 | A | SRC-002 labels both `930' LAND SPAN`. Independently in SRC-004's 1876 wire specification: "two side spans of 930 ft. each". |
| CTL-003 | bridge_proper_length | 3455.5 | ft | SRC-001 | A | "Length of bridge proper". Identity holds exactly: CTL-001 + 2 × CTL-002 = 3455.5. Checked at build time. |
| CTL-004 | total_length_including_approaches | 5989 | ft | SRC-001, SRC-002 | A | SRC-002: "OVERALL LENGTH OF BROOKLYN BRIDGE FROM PARK ROW, MANHATTAN, TO ADAMS ST., BROOKLYN, 5989 FT. (1996.3 YD)". |
| CTL-005 | manhattan_approach_length | 1562.5 | ft | SRC-002 | A | `1562'-6" MANHATTAN APPROACH`. **The approaches are asymmetric and both are dimensioned**, so no 50/50 split is guessed anywhere in this model. |
| CTL-006 | brooklyn_approach_length | 971 | ft | SRC-002 | A | `971' BROOKLYN APPROACH`. Identity holds exactly: CTL-005 + CTL-002 + CTL-001 + CTL-002 + CTL-006 = 5989 = CTL-004. Checked at build time; this is the strongest single internal check in the document. |

### 2.2 Elevations and clearance

| Control ID | Key | Value | Unit | Source IDs | Confidence | Notes |
|---|---|---:|---|---|---|---|
| CTL-010 | center_clearance_above_mhw | 135 | ft | SRC-001, SRC-002 | A | SRC-002 dimensions `135' MID SPAN CLEARANCE` directly off its `MEAN HIGH WATER` baseline. SRC-001: "Clear hgt. at mid-span above high water (90F) 135.0 ft." — the 90 °F qualifier is the thermal state at which the design clearance holds. |
| CTL-011 | roadway_clearance_at_tower_above_mhw | 110 | ft | SRC-002 | A | `110' CLEARANCE TO WATERLINE`, dimensioned from the `MEAN HIGH WATER` baseline up to the `ROADWAY` line at the Manhattan tower. It is **lower** than the 135 ft midspan clearance because the Brooklyn Bridge deck crests at the centre of the main span rather than sagging toward it — SRC-002's elevation draws that camber plainly. Used as the datum for the tower arch, see §4.2. |
| CTL-012 | manhattan_terminus_above_mhw | 36 | ft | SRC-002 | A | Park Row curb line, the Manhattan end of the approach. |
| CTL-013 | brooklyn_terminus_above_mhw | 68 | ft | SRC-002 | A | Adams Street curb line, the Brooklyn end of the approach. |
| CTL-014 | manhattan_approach_gradient | 0.0325 | ratio | SRC-001, SRC-002 | A | SRC-002: "3'-3" per hundred feet". SRC-001: "Grade of roadway 3.25%". Two sources, same number, expressed differently. |
| CTL-015 | brooklyn_approach_gradient | 0.0175 | ratio | SRC-002 | A | "THE BROOKLYN APPROACH REQUIRES A GRADIENT OF ONLY 1'-9" PER HUNDRED FEET." |
| CTL-016 | mid_channel_depth | 60 | ft | SRC-002 | A | `60' MID CHANNEL DEPTH`. Context for the river bed, not bridge structure. |
| CTL-017 | east_river_channel_width | 1950 | ft | SRC-002 | A | "1950' OVERALL WIDTH EAST RIVER CHANNEL". Context only. |

### 2.3 Towers

| Control ID | Key | Value | Unit | Source IDs | Confidence | Notes |
|---|---|---:|---|---|---|---|
| CTL-020 | tower_height_above_mhw | 276.5 | ft | SRC-002, SRC-003 | A | **ACTIVE tower height control.** SRC-002: `276'-6" OVERALL TO WATERLINE`. SRC-003: "the 276.5-foot towers". See CONF-001. |
| CTL-021 | tower_height_haer | 276.6 | ft | SRC-001 | A | SRC-001's figure. Recorded for traceability, **not used for geometry**; see CONF-001, where it is shown to be a decimalisation error for 276'-6". |
| CTL-022 | tower_extent_x_at_mhw | 59 | ft | SRC-002 | A | Tower masonry along the bridge axis at the mean high water line, dimensioned on the `ELEVATION TO EAST RIVER` view. |
| CTL-023 | tower_extent_y_at_mhw | 140 | ft | SRC-002 | A | Tower masonry transverse to the bridge at the mean high water line, dimensioned on the `ELEVATION TO MANHATTAN` view. Wider than the 85 ft deck, as expected. |
| CTL-024 | tower_count | 2 | count | SRC-001, SRC-002 | A | Manhattan and Brooklyn. |
| CTL-025 | tower_arch_count_per_tower | 2 | count | SRC-002, SRC-004 | A | SRC-004: "The three vertical shafts are connected by two pointed arches". |
| CTL-026 | tower_arch_width | 33.75 | ft | SRC-002, SRC-004 | A | SRC-002: `33'-9" ARCH WIDTH`. SRC-004: "a span of 33 feet 9 inches". SRC-001 gives 33.8 ft, the same figure decimalised. Three sources. |
| CTL-027 | tower_arch_depth_longitudinal | 21 | ft | SRC-004 | A | "…and a width of 21 feet", i.e. the through-thickness of the arch along the bridge axis. |
| CTL-028 | tower_arch_radius | 46 | ft | SRC-002 | A | `46' RADIUS`, annotated on the pointed arch of the Manhattan tower. |
| CTL-029 | tower_vault_height_above_roadway | 117 | ft | SRC-001, SRC-002 | A | SRC-002: `117' VAULT`, from the roadway line to the crown. SRC-001: "Height of arches above roadway 117.0 ft." |
| CTL-030 | tower_arch_height_above_springing | 36 | ft | SRC-002 | A | `36' ARCH HEIGHT`, measured from the springing course. **ACTIVE** for the arch derivation. See CONF-004. |
| CTL-064 | cable_saddle_drop_below_tower_top | 14.5 | ft | SRC-002 | B | **Scaled off the drawing, not stated on it.** Measured as a *ratio* on the orthographic elevation, so it is independent of any scale error: `(cable_y − towertop_y) / (MHW_y − towertop_y) × 276.5`. Both towers agree — Brooklyn 32 px below a 605 px tower, Manhattan 30 px below 580 px — giving 14.5 ft. The measurement chain is validated by a figure that played no part in setting it: the same scale puts the midspan deck underside at 133.9 ft against the drawing's own stated 135 ft. Graded `B`: grade-`A` material, but the scaling is this repository's derivation and a line on that sheet is about 5 ft thick. **Replaces a 0 ft placeholder, and supersedes a first attempt at 16.5 ft that mistook the flagstaff for the masonry cap.** |
| CTL-031 | tower_arch_rise_1877 | 35.5 | ft | SRC-004 | A | "two pointed arches which have a rise of 35 feet 6 inches". Recorded, **not used for geometry**. See CONF-004. |
| CTL-032 | tower_summit_above_foundation | 345 | ft | SRC-004 | A | "the summit of the New York tower is 345 feet above the foundation". Recorded, **not used for geometry** — SRC-004 does not say which surface it calls the foundation, and the arithmetic against CTL-020 and CTL-034 does not close. See OQ-004. |
| CTL-033 | caisson_depth_below_mhw_brooklyn | 44.5 | ft | SRC-001, SRC-002 | A | SRC-002: "THE BROOKLYN CAISSON RESTS AT 44'-6"". SRC-001: 44.5 ft. |
| CTL-034 | caisson_depth_below_mhw_manhattan | 78.5 | ft | SRC-001, SRC-002 | A | SRC-002: "THE CAISSON BELOW THE MANHATTAN TOWER COMES TO REST AT 78'-6"". SRC-001: 78.5 ft. **The two towers' foundations are at different depths and the model reflects that**; it does not average them. |
| CTL-035 | caisson_long_dimension_brooklyn | 168 | ft | SRC-005 | A | "The dimensions of the caisson are rectangular, length one hundred and sixty-eight feet, width one hundred and two feet". |
| CTL-036 | caisson_short_dimension | 102 | ft | SRC-005 | A | Same passage; SRC-005 gives 102 ft for both caissons. |
| CTL-037 | caisson_long_dimension_manhattan | 172 | ft | SRC-005 | A | "The dimensions of the base are one hundred and seventy-two feet by one hundred and two feet, covering an area of seventeen thousand five hundred and forty-four square feet. Its length is four feet greater than the Brooklyn caisson." 172 × 102 = 17,544 exactly — the source checks against itself. |
| CTL-038 | caisson_air_chamber_height | 9.5 | ft | SRC-005 | A | "height of air chamber nine feet six inches". |
| CTL-039 | caisson_roof_thickness | 15 | ft | SRC-005 | A | "making the roof of the caisson a solid mass of timber, of fifteen feet in thickness". |

### 2.4 Cables, suspenders and stays

| Control ID | Key | Value | Unit | Source IDs | Confidence | Notes |
|---|---|---:|---|---|---|---|
| CTL-040 | main_cable_count | 4 | count | SRC-001, SRC-002, SRC-003 | A | SRC-002: "FOUR MAIN CABLES CARRY THE DEAD AND LIVE LOADS OF THE SUPERSTRUCTURE." |
| CTL-041 | main_cable_diameter | 15.75 | in | SRC-001, SRC-002 | A | SRC-002: "the main cables reached their bound diameters of 15-3/4 inches". SRC-001: "Diameter over wrapping 15.75 in." See CONF-003. |
| CTL-042 | main_cable_length | 3578.5 | ft | SRC-001 | A | "Length of each cable". Includes the anchorage-embedded run; see the arc-length cross-check in §4.4. |
| CTL-043 | cable_wire_count | 5434 | count | SRC-001, SRC-002 | A | SRC-002: "THE FOUR MAIN BRIDGE CABLES WERE EACH COMPOSED OF 5,434 CONTINUOUS STEEL WIRES." See CONF-002. |
| CTL-044 | suspender_count | 1520 | count | SRC-001 | A | "Total number of vertical suspenders 1,520". |
| CTL-045 | diagonal_stay_count | 400 | count | SRC-001 | A | "Total number of diagonal stays 400". The stays are the Roebling system's defining second load path; SRC-002 annotates them: "DIAGONAL STAY CABLES CARRY PART OF THE SUSPENDED SUPERSTRUCTURE (THE DECK LOAD)." |
| CTL-046 | saddle_count | 8 | count | SRC-002 | A | "THE MAIN CABLES WERE CARRIED THROUGH THE TOWERS ON EIGHT CAST IRON SADDLE BEARINGS OF 13 TONS EACH." Four cables × two towers. |
| CTL-047 | cable_wire_count_1876_spec | 6300 | count | SRC-004 | A | Design-stage specification. Recorded, **not used**. See CONF-002. |
| CTL-048 | main_cable_diameter_1876_spec | 15 | in | SRC-004 | A | Design-stage specification. Recorded, **not used**. See CONF-003. |

### 2.5 Anchorages

All from SRC-004's description of the **New York** anchorage, the one it dimensions in full.
See OQ-006 on whether the Brooklyn anchorage matches.

| Control ID | Key | Value | Unit | Source IDs | Confidence | Notes |
|---|---|---:|---|---|---|---|
| CTL-050 | anchorage_extent_x | 129 | ft | SRC-002, SRC-004 | A | SRC-004: "The length over all the base of masonry is 129 feet." SRC-002 labels both anchorages `129'` in elevation. Two independent sources, one of them a measured drawing. |
| CTL-051 | anchorage_base_width_front | 106.333 | ft | SRC-004 | A | "The width at the front is 106 feet 4 inches". |
| CTL-052 | anchorage_base_width_rear | 116.333 | ft | SRC-004 | A | "…and at the rear 116 feet 4 inches." Consistent with the same passage's "widened at the rear by an offset of five feet on each side": 106'4" + 10' = 116'4". |
| CTL-053 | anchorage_rear_offset_station | 85.5 | ft | SRC-004 | A | "made at 85½ feet from the front" — where the plan steps out. |
| CTL-054 | anchorage_top_length | 117 | ft | SRC-004 | A | "The top surface … will have a length of 117 feet". |
| CTL-055 | anchorage_top_width_rear | 104.333 | ft | SRC-004 | A | "…and a width of 104 feet 4 inches, and 94 feet 4 inches at rear and front respectively." |
| CTL-056 | anchorage_top_width_front | 94.333 | ft | SRC-004 | A | Same sentence. |
| CTL-057 | anchorage_roadway_front_above_mhw | 89.04 | ft | SRC-004 | A | "The height of the roadway at front will be 89.04 feet". **The top of the anchorage is roadway** — SRC-004: "The top surface is to be sloped to the grade of the roadway, of which it will form part." |
| CTL-058 | anchorage_roadway_rear_above_mhw | 85.24 | ft | SRC-004 | A | Same sentence. |
| CTL-059 | anchorage_cornice_height | 12.583 | ft | SRC-004 | A | "There will be a cornice at top similar in design to those on the towers, of a full height of 12 feet 7 inches." |
| CTL-060 | anchorage_masonry_top_1875 | 78.5 | ft | SRC-004 | A | Brooklyn anchorage, "brought up to 78 feet 6 inches above high water". A **state of works**, not a finished height. Recorded, not used. See CONF-005. |
| CTL-061 | anchorage_count | 2 | count | SRC-001, SRC-002 | A | |
| CTL-062 | anchorage_eyebar_count | 1520 | count | SRC-001 | A | "Number of anchorage-chain eyebars 1,520". Identical to CTL-044; SRC-001 lists both as 1,520. Possibly correct, possibly a transcription collision in the source table. See OQ-011. |
| CTL-063 | anchorage_eyebar_length | 12 | ft | SRC-001, SRC-002 | A | SRC-001: "Average size of eyebars 12ft. x 3 in. x 8 in." SRC-002: "EIGHT LONG CHAINS OF 12-FOOT EYEBARS". |

### 2.6 Deck, trusses and floor system

| Control ID | Key | Value | Unit | Source IDs | Confidence | Notes |
|---|---|---:|---|---|---|---|
| CTL-070 | deck_width | 85 | ft | SRC-001, SRC-002 | A | SRC-001: "Clear width of bridge 85.0 ft." SRC-002 labels the deck `85' BRIDGE FLOOR` on the plan. |
| CTL-071 | floor_beam_length | 86 | ft | SRC-001 | A | One foot wider than the clear deck width, as expected for a beam carrying it. |
| CTL-072 | floor_beam_depth | 32 | in | SRC-001 | A | |
| CTL-073 | stiffening_truss_count_original | 6 | count | SRC-001, SRC-003 | A | SRC-003 quotes John Roebling's 1854 proposal directly: "…I have provided six lines of trusses." |
| CTL-074 | stiffening_truss_depth_inner_original | 17 | ft | SRC-001 | A | "Height of inner and intermediate trusses 17.0 ft." |
| CTL-075 | stiffening_truss_depth_outer_original | 8.7 | ft | SRC-001 | A | "Height of outer trusses 8.7 ft." The original outer trusses were half the depth of the inner ones. |
| CTL-076 | stiffening_truss_depth_present | 17 | ft | SRC-001 | A | SRC-001 note 2: "In the 1953 reconstruction of the suspended superstructure, the intermediate trusses were removed and the outer trusses were raised to the height of the inner trusses." All surviving trusses are therefore 17 ft deep. |
| CTL-077 | stiffening_truss_count_present | 4 | count | SRC-001 | B | **Reasoned, not stated.** Six trusses comprise two outer, two intermediate and two inner; SRC-001 note 2 says the intermediates were removed, leaving four. No read source states the number `4`. Graded `B` and flagged: see OQ-010. |
| CTL-078 | promenade_width_original | 15 | ft | SRC-003 | B | "a 15-foot-wide walkway", describing the original 1883 deck division. The present-day widths are CTL-088 to CTL-095 and are quite different. |

### 2.7 The promenade — SRC-011's longitudinal typology

NYC DOT's own 2016 study divides the promenade into eight named sections and dimensions each one.
This is the **owner** measuring the thing as it stands today, so every row here is grade `A`.

| Control ID | Key | Value | Unit | Source IDs | Confidence | Notes |
|---|---|---:|---|---|---|---|
| CTL-080 | promenade_length_concrete_approaches | 2365 | ft | SRC-011 | A | "Concrete Approaches - 2365 feet: 35%". Both ends combined. |
| CTL-081 | promenade_length_wood_deck_approaches | 750 | ft | SRC-011 | A | "Wood Deck Approaches - 750 feet: 11%". |
| CTL-082 | promenade_length_wood_deck_with_cables | 1510 | ft | SRC-011 | A | "Wood Deck with Cables – 1,510 feet: 23%". The stretch where the main cables descend alongside the path. |
| CTL-083 | promenade_length_tower_ramps | 540 | ft | SRC-011 | A | "Tower Ramps - 540 feet: 8%". Four ramps, two at each tower. |
| CTL-084 | promenade_length_towers | 109 | ft | SRC-011 | A | "Towers - 109 feet: 2%". The passage through both towers. |
| CTL-085 | promenade_length_crown | 355 | ft | SRC-011 | A | "Crown – 355 feet: 5%". The high point at midspan. |
| CTL-086 | promenade_length_trunk_cable_bases | 114 | ft | SRC-011 | A | "Trunk Cable Bases - 114 feet, 2%". Where the cables reach path level — the narrowest points on the bridge. |
| CTL-087 | promenade_length_brooklyn_curve | 910 | ft | SRC-011 | A | "Brooklyn Curve - 910 feet: 14%". **The section that carries the promenade past the bridge's Adams Street terminus toward Tillary Street and Boerum Place (SRC-012), and the section that holds the Washington Street staircase.** See CONF-007. |
| CTL-088 | promenade_width_concrete_approach | 17 | ft | SRC-011 | A | "1. CONCRETE APPROACHES 17'". The widest section. |
| CTL-089 | promenade_width_wood_deck_approach | 16 | ft | SRC-011 | A | "Width of 16' is generally acceptable for a shared use path." |
| CTL-090 | promenade_width_wood_deck_with_cables | 13 | ft | SRC-011 | A | "Cable supports connect inside of fence narrowing effective width of pathway 13'". |
| CTL-091 | promenade_width_tower_ramp | 12 | ft | SRC-011 | A | "Approaching tower, fence moves from outside of cables to inside, narrowing path further 12'". |
| CTL-092 | promenade_width_at_towers | 43 | ft | SRC-011 | A | "5. TOWERS 43'". The path opens out into the tower balconies. |
| CTL-093 | promenade_width_crown | 16 | ft | SRC-011 | A | "6. CROWN … 16'". |
| CTL-094 | promenade_width_trunk_cable_base | 10 | ft | SRC-011 | A | "Narrowest point on bridge is at trunk cable bases where the path is 10'". |
| CTL-095 | promenade_width_brooklyn_curve | 11 | ft | SRC-011 | A | "8. BROOKLYN CURVE … 11'", annotated "Narrow path, excess space on north side of fence to accommodate staircase". **This is the sourced statement that puts the staircase in this section.** |
| CTL-096 | promenade_below_girder_height | 4 | ft | SRC-011, SRC-015 | A | "The majority of the wood deck is 4' below girders except at the towers and tower ramps" — 79% of the length. Independently in SRC-015. |
| CTL-097 | promenade_elevation_above_roadway | 18 | ft | SRC-015 | B | The promenade sits 18 ft above the automobile lanes. **Graded `B`, not `A`**: no primary or owner document read here states it, and SRC-015 is tertiary. It supersedes a 12 ft placeholder. SRC-011's grade-`A` "4 ft below girders" (CTL-096) is the relationship that will replace this once a girder elevation is registered — see OQ-013. |
| CTL-098 | vehicle_lane_count | 5 | count | SRC-011 | A | Present-day. NYC DOT: the bridge "supports five lanes of vehicles (no trucks), a pedestrian promenade and protected bike lane". SRC-011's 2016 history page says six lanes; one was taken for the bike lane in 2021. See CTL-099. |
| CTL-099 | bike_lane_opened_year | 2021 | count | SRC-011 | A | September 2021: a two-way protected bike lane replaced the leftmost Manhattan-bound vehicle lane, and the promenade became **pedestrian-only**. Recorded as a date, not a dimension; it is what makes CTL-098 current rather than historic. |

---

## 3. Placeholder parameters — NOT dimensional facts

Same column contract. **Every row here is confidence `D`** and cites no source. These are shape
hints. They must not be quoted as dimensions, exported as measurements, or used to validate an
imported mesh. Every part that depends on one of these is rendered with a dotted outline and is
excluded from dimension callouts.

**Placeholder values are also chosen not to collide with a negative control.** Tests `STT-005` and
`STT-006` scan every control value against the Manhattan and Williamsburg Bridge figures, and they
caught three placeholders here on their first run — a 40 ft truss offset against Williamsburg's 40 ft
truss depth, and a 120 ft tower width against Manhattan's 120 ft deck. Those were changed rather than
exempted. An arbitrary number that happens to look like a forbidden one blunts the guard, and a
placeholder is arbitrary by definition, so there is no cost to moving it.

| Control ID | Key | Value | Unit | Source IDs | Confidence | Notes |
|---|---|---:|---|---|---|---|
| CTL-101 | min_suspender_length_at_midspan | 3 | ft | none | D | PLACEHOLDER, and now **bounded by measurement**. Scaling SRC-002 puts the cable's lowest point at about 150 ft above mean high water, against a derived truss top chord at 152 ft — so this gap is within a couple of feet of zero, which is what the row already assumed. It stays a placeholder because no source states it and the scaling is good only to about ±5 ft. See OQ-001. |
| CTL-102 | cable_saddle_drop_below_tower_top_placeholder_retired | 0 | ft | none | D | **RETIRED.** Superseded by CTL-064, which is scaled off SRC-002 at 16.5 ft. Kept at zero and referenced by nothing, so the retirement is visible in the diff rather than silent. |
| CTL-103 | deck_structure_depth | 3 | ft | none | D | PLACEHOLDER. Structural depth of the roadway deck above the truss bottom chord. See OQ-013. |
| CTL-104 | truss_offset_outer | 38 | ft | none | D | PLACEHOLDER. Transverse offset of the two outer stiffening trusses from the centerline. **Bounded**: the deck is 85 ft wide (CTL-070) so this cannot exceed 42.5 ft. See OQ-002. |
| CTL-105 | truss_offset_inner | 15 | ft | none | D | PLACEHOLDER. Transverse offset of the two inner stiffening trusses. Bounded above by CTL-104. See OQ-002. |
| CTL-106 | brooklyn_curve_terminus_drop | 15.9 | ft | none | D | PLACEHOLDER, but bounded and not arbitrary. The Brooklyn Curve descends past Adams Street toward Tillary/Boerum (SRC-011, SRC-012). Its 910 ft length is grade `A` (CTL-087); carrying it down at this bridge's own sourced Brooklyn approach gradient (CTL-015, 1.75%) gives 15.9 ft of fall. **The gradient is sourced, applying it here is reasoning.** See OQ-014. |
| CTL-107 | stair_width | 12 | ft | none | D | PLACEHOLDER. The Brooklyn staircase down to Washington Street, and the Manhattan approach staircase. **Their existence and location are grade `A`/`B`** — SRC-011 annotates both as pinch points and puts the Brooklyn one in the Brooklyn Curve; SRC-012 and SRC-013 name the streets; SRC-014 is direct testimony. Only the *size* is a guess, which is exactly why these parts are `INFERRED` and not `ASSUMED`. See OQ-015. |
| CTL-108 | tower_extent_x_at_top | 42 | ft | none | D | PLACEHOLDER. The towers taper. SRC-002 draws the taper but dimensions the plan only at mean high water (CTL-022, CTL-023). See OQ-004. |
| CTL-109 | tower_extent_y_at_top | 116 | ft | none | D | PLACEHOLDER. As above, transverse. See OQ-004. |
| CTL-110 | approach_bent_spacing | 100 | ft | none | D | PLACEHOLDER. Longitudinal spacing of approach supports, chosen only so the approaches read as supported viaducts rather than floating slabs. The **extent** they are applied over is grade `A` (CTL-005, CTL-006); the **rhythm** is not. SRC-004 describes the Brooklyn approach as brick piers and arches over blocks of roughly 250 ft, which suggests this is the right order of magnitude and nothing more. See OQ-007. |
| CTL-111 | approach_bent_width_x | 8 | ft | none | D | PLACEHOLDER. See OQ-007. |
| CTL-112 | approach_girder_depth | 10 | ft | none | D | PLACEHOLDER. See OQ-007. |

---

## 4. Derivation rules

Computed by `scripts/build_control_skeleton.py` from the tables above. `ft2m = 0.3048`.
Each derived quantity inherits the **weakest** grade among its inputs.

### 4.1 Longitudinal stations (X, meters)

| Station ID | Rule | Confidence | Note |
|---|---|---|---|
| STA-MID | `0` | A | Origin, main span midpoint. |
| STA-TWR-M | `−main_span / 2` | A | Manhattan tower centerline. |
| STA-TWR-B | `+main_span / 2` | A | Brooklyn tower centerline. |
| STA-ANC-M | `−(main_span / 2 + side_span_each)` | A | Manhattan anchorage cable point. |
| STA-ANC-B | `+(main_span / 2 + side_span_each)` | A | Brooklyn anchorage cable point. |
| STA-APPR-END-M | `STA-ANC-M − manhattan_approach_length` | A | Park Row. **Grade A, not a guess** — SRC-002 dimensions each approach separately. |
| STA-APPR-END-B | `STA-ANC-B + brooklyn_approach_length` | A | Adams Street. |
| STA-ANC-M-REAR / B-REAR | `STA-ANC-M/B −/+ anchorage_extent_x` | A | Landward face of each anchorage block. |

**Where the anchorage block sits in the chain.** SRC-002's five lettered dimensions sum to its own
stated 5989 ft with **zero residual**, and the 129 ft anchorage is not one of the five. The block
must therefore lie *inside* one of them. It is placed inside the approach dimension, so that the
tower-to-anchorage side span stays at the 930 ft that SRC-001, SRC-002 and SRC-004 all state. The
alternative — putting it inside the land span — would silently shorten the side span to 801 ft and
contradict three sources. This reading is checked, not assumed: see CHK-003 and CHK-004 below.

Two identities are asserted at build time, and both close exactly:

```text
main_span + 2 * side_span_each                             == bridge_proper_length      (3455.5 ft)
bridge_proper_length + manhattan_approach + brooklyn_approach == total_length            (5989 ft)
```

The second is the strongest check in this document: five independently lettered dimensions from a
measured drawing sum to that drawing's own stated overall length with zero residual.

A third and fourth check test the *interpretation* rather than the arithmetic. The approach roadway
runs from its terminus to the landward face of the anchorage — `approach_length − anchorage_extent_x`
— at a sourced gradient, and must arrive at the sourced anchorage roadway level:

```text
manhattan_terminus + manhattan_gradient * (manhattan_approach − anchorage_extent_x)  ==  anchorage_roadway_rear
brooklyn_terminus  + brooklyn_gradient  * (brooklyn_approach  − anchorage_extent_x)  ==  anchorage_roadway_rear
```

Both land about **2.5 ft low, with the same sign**. That common offset is more persuasive than an
exact hit on one side would be: it looks like a systematic difference between the curb-line
elevations SRC-002 tabulates and the roadway grade line SRC-004 quotes, rather than an error in the
chain. It is recorded, not tuned away, and the tolerance is set at 1 m so that a real drift of a
different character would still fail.

### 4.2 Elevations (Z, meters relative to MHW)

| Elevation ID | Rule | Confidence | Note |
|---|---|---|---|
| ELV-FOUNDATION-M | `−caisson_depth_below_mhw_manhattan` | A | −78.5 ft. |
| ELV-FOUNDATION-B | `−caisson_depth_below_mhw_brooklyn` | A | −44.5 ft. **Asymmetric by 34 ft**, and modelled that way. |
| ELV-DATUM | `0` | A | Mean high water. |
| ELV-CLEARANCE | `center_clearance_above_mhw` | A | 135 ft, underside of the suspended structure at midspan. |
| ELV-TRUSS-BOTTOM | `ELV-CLEARANCE` | B | Bottom chord taken at the clearance plane. The clearance is grade `A`; equating it with the chord is reasoning. |
| ELV-TRUSS-TOP | `ELV-CLEARANCE + stiffening_truss_depth_present` | A | 152 ft. Both inputs grade `A`. |
| ELV-DECK | `ELV-TRUSS-BOTTOM + deck_structure_depth` | D | Placeholder depth. |
| ELV-PROMENADE | `ELV-DECK + promenade_elevation_above_roadway` | B | 18 ft above the roadway (CTL-097). Was a `D` placeholder at 12 ft before SRC-011 and SRC-015 were read. |
| ELV-TOWER-TOP | `tower_height_above_mhw` | A | 276.5 ft. |
| ELV-SADDLE | `ELV-TOWER-TOP − cable_saddle_drop_below_tower_top` | B | 276.5 − 16.5 = 260.0 ft. CTL-064 is scaled off the drawing, so the saddle is grade `B` rather than the `D` it was when the drop was a zero placeholder. |
| ELV-CABLE-MID | `ELV-TRUSS-TOP + min_suspender_length_at_midspan` | D | **Derived, not guessed**: the cable must meet the top chord at midspan where the suspenders reach minimum length. |
| ELV-ANCHOR-POINT | `anchorage_roadway_front_above_mhw` | A | 89.04 ft. The cable enters the anchorage at the top of the block, which SRC-004 states is roadway level. |
| ELV-TOWER-ROADWAY | `roadway_clearance_at_tower_above_mhw` | A | 110 ft. Used only as the datum for the tower arch, per SRC-002's own `ROADWAY` line. |
| ELV-ARCH-CROWN | `ELV-TOWER-ROADWAY + tower_vault_height_above_roadway` | A | 227 ft. Both inputs grade `A`, both from SRC-002. |

**Derived main-span sag** = `ELV-SADDLE − ELV-CABLE-MID` = 260.0 − (135 + 17 + 3) = **105.0 ft**,
a sag ratio of 1 : 15.2.

**An earlier version of this document called that ratio evidence of an error. That judgement was
wrong, and the correction is worth recording.** The argument was that suspension bridges sit in a
1:7 to 1:12 band, so anything shallower indicated a bad placeholder. That band describes a *pure*
suspension bridge, in which the cable carries everything. The Brooklyn Bridge is not one. Its
diagonal stays are a second load path — SRC-002 annotates them "DIAGONAL STAY CABLES CARRY PART OF
THE SUSPENDED SUPERSTRUCTURE (THE DECK LOAD)" — and a stayed system tolerates, and wants, a
shallower cable. Applying a rule of thumb from a different structural type was the mistake, not the
geometry.

**What the drawing actually says.** SRC-002 is orthographic with a dimensioned 1595.5 ft main span,
which fixes the scale of the 14484 px master at 0.4824 ft per pixel. Measured on that basis:

| Measured off SRC-002 | Result | Model |
|---|---:|---:|
| Tower cornice above MHW | 276.5 ft *(used to set the scale)* | 276.5 ft |
| Cable crossing the tower — the saddle | ≈ 260 ft | 260.0 ft |
| Cable's lowest point at midspan | ≈ 150 ft | 155.0 ft |
| **Sag** | **≈ 110 ft, 1 : 14.5** | **105.0 ft, 1 : 15.2** |

The model and the drawing agree to about 5 ft on a 1595 ft span, which is inside the ±5 ft the
scaling can resolve. The saddle drop that came out of this — 16.5 ft, CTL-064 — has replaced a
0 ft placeholder, and the sag improved from 121.5 ft to 105.0 ft in the process.

**This does not close OQ-001.** A number scaled off a drawing is not a number stated by a source, and
the cable system is still graded on CTL-101, which remains a placeholder. What changed is that the
sag is now *bounded by a measurement* rather than resting entirely on two guesses.

**Arc-length cross-check against CTL-042.** A parabola of 1595.5 ft span and 105 ft sag has an arc
length of about 1614 ft; two side-span chords add roughly 940 ft each; the total is about 3494 ft
against a stated 3578.5 ft per cable. The 84 ft residual is the run embedded in the two anchorages,
about 42 ft per end. A **consistency check, not a determination** — cable length is only weakly
sensitive to sag, which is exactly why it could not settle OQ-001 either.

### 4.3 Transverse layout (Y, meters)

| Item | Rule | Confidence |
|---|---|---|
| Deck edges | `± deck_width / 2` | A |
| Floor beam ends | `± floor_beam_length / 2` | A |
| Outer trusses / outer cables | `± truss_offset_outer` | D |
| Inner trusses / inner cables | `± truss_offset_inner` | D |
| Tower masonry at MHW | `± tower_extent_y_at_mhw / 2` | A |

**The four cables are placed above the four present-day trusses.** That is the Roebling arrangement
and SRC-002 draws it, but the *offsets* are placeholders, so every cable and every truss in this
model is `INFERRED` in Y and `DOCUMENTED` in X and Z. The metadata records that asymmetry rather
than flattening it to a single grade.

### 4.4 Curves

| Curve | Rule | Confidence |
|---|---|---|
| Main cable, main span | Parabola through `(±main_span/2, ELV-SADDLE)` with vertex `(0, ELV-CABLE-MID)` | D |
| Main cable, side spans | Straight chord, saddle to `ELV-ANCHOR-POINT` at the anchorage station | D |
| Suspender pitch | `bridge_proper_length / (suspender_count / main_cable_count)` = 3455.5 / 380 = 9.09 ft | B |
| Deck chain | Continuous from `STA-APPR-END-M` to `STA-APPR-END-B` | A |

**On the suspender pitch.** The count (CTL-044) is grade `A`; dividing it evenly over the suspended
length is reasoning, not a source statement, so the pitch is `B` and every suspender is `INFERRED`.

**On the deck chain.** SRC-004 states that the anchorage top surface *is* roadway, and SRC-002 draws
an unbroken deck from Park Row to Adams Street. The deck must therefore be continuous across the
anchorages and along both approaches — not stop at the anchorage face where the *suspended* structure
ends. Test `GRT-030` asserts there is no longitudinal gap anywhere in the chain. This is the single
most expensive bug recorded in `HOW-TO-DESIGN.md` §11 and the test exists before the deck did.

### 4.5 The promenade chain, and where it stops

The promenade is **not** co-terminous with the roadway, and getting that wrong was a real defect in
this model's first build, where the walkway simply ended at Adams Street with the road.

| Segment | Extent | Width control | Confidence |
|---|---|---|---|
| Manhattan concrete approach | Park Row → Manhattan anchorage | CTL-088, 17 ft | A |
| Manhattan side span | anchorage → tower | CTL-090, 13 ft | A |
| Manhattan tower balcony | at the tower centerline | CTL-092, 43 ft | A |
| Main span, Manhattan half | tower → crown | CTL-090, 13 ft | A |
| Crown | 355 ft centred on midspan | CTL-093, 16 ft | A |
| Main span, Brooklyn half | crown → tower | CTL-090, 13 ft | A |
| Brooklyn tower balcony | at the tower centerline | CTL-092, 43 ft | A |
| Brooklyn side span | tower → anchorage | CTL-090, 13 ft | A |
| Brooklyn concrete approach | anchorage → Adams Street | CTL-088, 17 ft | A |
| **Brooklyn Curve** | **Adams Street → 910 ft beyond it** | CTL-095, 11 ft | A length and width, `D` fall |

The section lengths are grade `A` as totals, but their **split between the two ends** is reasoning,
and so is the placement of each section along the bridge. Every promenade segment is therefore
`INFERRED`, including the crown: SRC-011 gives the crown as 355 ft, but **it does not say the crown
is centred on midspan** — that is inference from the cable profile, and the build derives `INFERRED`
accordingly rather than taking credit for a grade-`A` position.

**Consistency check CHK-006.** SRC-011's typologies that sit on the 1883 structure — everything
except the concrete approaches and the Brooklyn Curve — sum to:

```text
750 + 1510 + 540 + 109 + 355 + 114  =  3378 ft
bridge_proper_length (CTL-003)      =  3455.5 ft      residual 77.5 ft, 2.2%
```

A 2016 pedestrian study by the city and a 1980s HAER measured drawing of an 1883 structure agree on
the length of the suspended bridge to within 78 ft, having been produced for entirely different
purposes. Neither was derived from the other. The residual is small and positive in the direction you
would expect, since the wood deck starts a little inside the anchorage faces.

**The horizontal curve is not modelled.** SRC-011 calls this section the Brooklyn *Curve*, and
SRC-014 describes the roadway diverging while the walkway continues in the middle. No read source
gives the curve's radius or bearing, so the model runs it **straight** along the centerline, which is
where the walkway sits relative to the road it is separating from. That is a known, registered
omission — OQ-014 — not an oversight.

---

## 5. Open questions

| ID | Question | Blocks | Retired by |
|---|---|---|---|
| OQ-001 | What is the main cable sag at midspan? CTL-064 now scales the saddle drop off the drawing, but nothing *states* it, and CTL-101 is still a placeholder. | CTL-101, the cable system's grade | J. A. Roebling's 1867 design report; NYCDOT record drawings |
| OQ-002 | Where are the four present-day stiffening trusses transversely? | CTL-104, CTL-105 | NYCDOT drawings; a dimensioned section |
| OQ-003 | What is the present-day deck arrangement — lanes, Promenade, the 2021 bike lane? | Any deck subdivision | **Largely answered by SRC-011.** Five vehicle lanes, no trucks; a two-way protected bike lane on the Manhattan-bound roadway since September 2021; the promenade pedestrian-only since then. The **transverse position** of each lane is still unregistered, so the deck is still modelled as a single envelope. |
| OQ-013 | How high is the promenade above the roadway, exactly, and how deep is the deck structure? | CTL-097, CTL-103 | **Half answered.** SRC-011 gives the promenade as 4 ft below the girders (CTL-096, grade `A`), but no read source gives the girder elevation, so the model uses SRC-015's 18 ft above the roadway at grade `B`. Registering a girder elevation would replace a `B` with an `A`. Promenade *widths* are now fully sourced and this question no longer covers them. |
| OQ-014 | What is the Brooklyn Curve's horizontal alignment — radius, bearing, and where exactly does the roadway diverge from it? | The curve is modelled **straight**; its 910 ft length and 11 ft width are grade `A`, its plan geometry is absent | NYCDOT record drawings; aerial imagery; the 2017 LiDAR |
| OQ-015 | What are the dimensions of the Washington Street staircase and the Manhattan approach staircase? | CTL-107 | NYCDOT drawings. Their existence and street locations are already sourced (SRC-011, SRC-012, SRC-013, SRC-014); only the size is open. **The SRC-018 review returned zero `stair` photographs out of 252 decisions**, so this question is not merely still open — it is now known to be unreachable by photo crowd-sourcing of bridge imagery, and needs a targeted DUMBO street-level collection or the drawings. |
| OQ-016 | How is the tower masonry above the saddle actually arranged, and how wide is the opening the cables pass through? | The width of the cornice opening, and therefore how much of the tower top reads as solid | NYCDOT drawings; SRC-007 plates of the tower tops. SRC-002 establishes that the cables are carried *through* the towers, so the band cannot be solid across them — but nothing read dimensions the opening. **Half-answered by the SRC-018 review**: fourteen accepted `cornice` photographs show the arrangement plainly — the tower top carries raised blocks at the four corners, outboard of the outer cables, with the masonry stepping down between them so each cable passes over a saddle in the gap. That is the arrangement the model already builds, so the review *confirms an inference* rather than changing geometry. The width is still unmeasured, and a photograph cannot supply it. |
| OQ-017 | Where is the suspended deck at each tower? | CTL-011 | Scaling SRC-002's elevation puts the deck underside at roughly 117 ft at the Manhattan tower and 124 ft at the Brooklyn tower, against the 110 ft that SRC-002's own tower detail annotates. See CONF-008. |
| OQ-004 | How do the towers taper, and what surface does SRC-004 call "the foundation" in its 345 ft statement? | CTL-108, CTL-109, CTL-032, CONF-004 | Municipal Archives tower drawings |
| OQ-005 | Which caisson axis is which? 168 ft and 102 ft are sourced; the assignment to transverse/longitudinal is reasoned from the tower being 140 ft × 59 ft and having to sit on it. | Caisson orientation | SRC-005 plates; Municipal Archives |
| OQ-006 | Is the Brooklyn anchorage the same size as the New York one? SRC-004 dimensions only New York; SRC-002 labels both `129'`. | Anchorage symmetry | SRC-004's Brooklyn sections; NYCDOT |
| OQ-007 | What carries the approach viaducts, and at what spacing? | CTL-110, CTL-111, CTL-112 | **The model's supports are the wrong *kind* of thing, not merely the wrong size.** SRC-004 describes brick piers and arches, and SRC-016's modern photography shows a masonry arcade carrying the approach, not a line of slender bents. The model draws bents because nothing dimensions the arcade. Retired by NYCDOT drawings. **The SRC-018 review returned zero `arcade` photographs out of 252 decisions** — the campaign asked for them explicitly and the openly-licensed corpus does not contain them, because people photograph the bridge from the promenade and the waterfront, not the viaduct they drive under. This question was the campaign's primary target and the campaign failed to reach it; that is a finding about the method, not a reason to soften the grade. |
| OQ-008 | What is the real-world azimuth and origin of the bridge axis? SRC-008's coordinate locates the LOC record, not a structural element, so it cannot verify a placement. | Georeferencing, any district integration | Survey control; LiDAR |
| OQ-009 | What is the offset between mean high water and NAVD88 at this location? | Any geodetic vertical placement | **Answered by SRC-010**: the canonical frame declares `MHW = NAVD88 + 0.59 m` within a 4000 m radius that covers this bridge. Recorded and deliberately **not applied** — the model stays in MHW because that is the datum its sources use, and the conversion belongs at placement time. |
| OQ-010 | How many trusses were removed in 1953, and what is the resulting section? | CTL-077 | 1953 reconstruction drawings |
| OQ-011 | Are the 1,520 eyebars and the 1,520 suspenders genuinely the same number, or a collision in SRC-001's table? | CTL-062 confidence | Vogel 1983 directly |
| OQ-012 | The brief asks for four subway tracks. The Brooklyn Bridge carries no rail lines at all. | Nothing — resolved by not modelling any rail | **Closed.** Neither the Manhattan Bridge's subway tracks nor this bridge's own elevated and trolley tracks — removed in the mid-twentieth century — are modelled. Registered as SRC-902, enforced by `STT-008`. |

---

## 6. Material assignments

Matched in **document order**; the first glob that matches a `part_id` wins, so the table runs from
most specific to least. **There is no default rule.** A part that matches nothing is a build failure,
not a silent grey — see `scripts/control_model.py::material_for`.

| Material ID | Applies to | Material | Source IDs | Confidence | Notes |
|---|---|---|---|---|---|
| MAT-001 | `tower_*_caisson*` | concrete | SRC-005 | A | Timber caisson filled with concrete after landing; SRC-005 describes the filling of the air chamber. Rendered as concrete. |
| MAT-002 | `tower_*` | masonry | SRC-002, SRC-004 | A | SRC-002 annotates the coursing directly: "TOWER STONES IN THE VERTICAL COURSES ARE QUARRY FACED, WITH THE CORNERS DRAFT-CHISELED TO SQUARE." SRC-004 specifies granite and limestone by course. |
| MAT-003 | `anchorage_*` | masonry | SRC-002, SRC-004 | A | SRC-004: granite corners, cornice and curtain arches, over limestone backing. |
| MAT-004 | `cable_main_*` | steel_wire | SRC-002, SRC-003 | A | SRC-003: "the first time that galvanized steel wire was used in cable construction". |
| MAT-015 | `saddle_*` | steel_structural | SRC-002 | A | SRC-002: "EIGHT **CAST IRON** SADDLE BEARINGS OF 13 TONS EACH". Cast iron is not in the closed material vocabulary; `steel_structural` is its nearest member and the distinction is recorded here rather than lost. |
| MAT-005 | `suspender_*` | steel_wire | SRC-001, SRC-002 | A | |
| MAT-006 | `stay_*` | steel_wire | SRC-001, SRC-002 | A | Diagonal stays. |
| MAT-007 | `truss_*` | steel_structural | SRC-003 | A | SRC-003: "the suspension system was initially designed in iron, but was changed to steel". |
| MAT-008 | `floor_beam_*` | steel_structural | SRC-001 | A | |
| MAT-009 | `deck_*` | asphalt | SRC-018 | B | Was `roadway_surface`/`D`. Eighteen photographs accepted in the SRC-018 review are tagged `deck`, and the roadway reads unambiguously as bituminous pavement with painted lane markings in every one — including driver's-eye views on the bridge proper. `B`, not `A`: a reviewer observed a surface, which is not the same as a specification stating one, and a wearing course is renewed on a maintenance cycle rather than being an as-built fact. |
| MAT-010 | `promenade_*` | timber | SRC-018 | B | Was `roadway_surface`/`D`, on the grounds that SRC-011's "wood deck" is a *typology name* and reading it as a materials statement would be the exact over-claim this axis exists to prevent. That reasoning was right and is now moot: twelve accepted photographs show transverse timber planking directly, so the claim rests on the planks and not on the label. This is the placeholder the photo campaign was built to retire. |
| MAT-011 | `approach_*` | masonry | SRC-004 | B | SRC-004 describes the Brooklyn approach as brick piers and arches; the Manhattan approach is not described in the passages read. |
| MAT-012 | `station_*` | reference | none | D | Non-physical reference markers. |
| MAT-014 | `stair_*` | steel_structural | none | D | The staircases exist and are located (SRC-011 puts the Brooklyn one in the Brooklyn Curve; SRC-012 and SRC-013 name the streets; SRC-014 is direct testimony). Nothing read says what they are made of. **Stays `D` after the SRC-018 review**: the campaign offered a `stair` category precisely to close this, and the reviewer tagged it zero times in 252 decisions. A corpus harvested from bridge photography contains almost no pictures of the thing at the *bottom* of the bridge. See OQ-015. |
| MAT-013 | `*` | reference | none | D | **Catch-all for reference geometry only.** Placed last, and deliberately mapped to `reference` so that a real structural part accidentally falling through reads as an obviously wrong ghost in the viewer rather than as plausible grey stone. |

---

## 7. Geometry provenance — how the shape is known

Derived per part in the build, never declared here. The rule is in
[CONFIDENCE-MODEL.md](CONFIDENCE-MODEL.md) §2. Expected distribution at Milestone 1:

```text
MEASURED   0    no survey or photogrammetry has been ingested
DOCUMENTED >0   the span chain, tower elevations and extents, anchorage block, arches
INFERRED   >0   cables, suspenders, trusses, promenade, deck depth
ASSUMED    >0   approach viaduct supports
```

`MEASURED == 0` is computed, not hardcoded, and reported by `GRT-020` without failing the build — so
that the day a survey lands, the number changes on its own.
