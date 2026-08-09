# Brooklyn Bridge Digital Twin

A source-governed, part-addressable control skeleton of the Brooklyn Bridge, built for browser
rendering and HO-scale study.

**Every dimension in this model traces to a registered source with an explicit confidence grade.
Anything unsourced is graded `D`, labelled a placeholder, drawn with a dotted outline, and linked to
a named open question.**

```powershell
python scripts/build_control_skeleton.py     # emit GLB + metadata from GEOMETRY-CONTROL.md
python scripts/validate_dimensions.py        # 36 tests
python scripts/prove_guards.py               # prove the guards fail on the defects they catch
cd viewer; npm install; npm run dev          # http://localhost:5174
```

---

## Milestone 1 — where this stands

| | |
|---|---|
| Controls | **78** — 66 sourced (64 grade `A`, 2 grade `B`), 12 placeholders |
| Sources read | **8**, including two period primaries and the only measured drawing of any East River suspension bridge in the national record |
| Parts | **93** across 8 systems |
| Provenance | 0 measured · 11 documented · 80 inferred · 2 assumed |
| Tests | **36** — 32 asserting, 4 report-only, **0 failing** |
| Guards proven | 9 injected defects, each confirmed to fail its guard |
| Registered conflicts | 6 — four settled with reasoning, two left open |
| Open questions | 13 — one closed, one answered by the shared contract |

Turning `INFERRED` and `ASSUMED` off in the viewer leaves the two anchorages and the seven station
markers. **That emptiness is the honest picture of what these sources actually locate**, and it is
published rather than hidden.

---

## What the sources gave us

The Brooklyn Bridge is the luckiest of the three East River bridges in the national record, and this
milestone spent its effort collecting that advantage rather than guessing.

**HAER No. NY-18 sheet 1 of 1 — the measured drawing.** Read at full resolution by cropping the
14484 × 9632 px master. It is datumed to `MEAN HIGH WATER`, and it dimensions the whole span chain:

```text
1562'-6" MANHATTAN APPROACH | 930' LAND SPAN | 1595'-6" MAIN SPAN | 930' LAND SPAN | 971' BROOKLYN APPROACH
                     "OVERALL LENGTH ... FROM PARK ROW ... TO ADAMS ST., BROOKLYN, 5989 FT."
```

Those five numbers sum to 5989 **exactly**. That identity is asserted at build time (`GRT-011`) and
it is the strongest check in the repository — it also settles where the 129 ft anchorage block sits
in the chain, because the sum leaves no room for it anywhere else.

**Washington Roebling's own reports, 1873 and 1877.** Period primaries, read as full text. They give
the New York anchorage in complete plan and elevation — 129 ft long, 106'4" wide at the front,
116'4" at the rear, roadway at 89.04 ft above high water — and both caisson footprints, with the
source checking itself: *"one hundred and seventy-two feet by one hundred and two feet, covering an
area of seventeen thousand five hundred and forty-four square feet"*, which multiplies out precisely.

**Three checks that did not have to pass, and did.** Each is a different pair of sources meeting:

| Check | Residual |
|---|---|
| Approach gradient chains, from both termini to the sourced anchorage roadway level | −2.65 ft and −2.51 ft — the same sign and size, which reads as a systematic curb-line versus grade-line offset rather than an error |
| A two-centred arch of the sourced radius (46 ft) spanning the sourced width (33'-9") reaching the sourced arch height (36 ft) | −0.39 ft |
| Span chain against the drawing's own stated overall length | 0.000 ft |

**A conflict resolved by arithmetic, not preference.** HAER's data pages give the tower height as
`276.6 ft`; the measured drawing says `276'-6"` and ASCE says `276.5`. HAER decimalises its other
feet-and-inches values correctly — 44'-6" → 44.5, 78'-6" → 78.5, 33'-9" → 33.8 — so its `276.6` is a
digit error. The model uses 276.5, records 276.6 as CTL-021, and `GRT-061` fails if the recorded
figure ever reaches the geometry.

All six conflicts, including the two that remain open, are in [SOURCE-REGISTER.md](SOURCE-REGISTER.md).

---

## Where this model departs from the brief

[AGENT-INSTRUCTIONS.md](AGENT-INSTRUCTIONS.md) was adapted from the Manhattan Bridge's brief, and the
adaptation left residue. Two departures are deliberate and both are enforced by tests.

**1. No rail lines. Not four subway tracks, not any.** The brief's §6 taxonomy and §13 milestone ask
for `subway_tracks: [track_1 … track_4]`. That is a Manhattan Bridge feature. **The Brooklyn Bridge
carries no rail.** ASCE records that the *original* 1883 deck was divided to give "two elevated
railroad tracks, two trolley car tracks, a single-lane road, and a 15-foot-wide walkway" — that rail
was removed in the mid-twentieth century, and none of it was ever subway. Nothing rail-related is
modelled; the historic arrangement is registered as context only. `STT-008` forbids `subway`, `rail`,
`trolley`, `elevated` and `track_n` in any part ID. What was built in their place is the system the
brief omitted and this bridge actually needs: the **diagonal stays**, which the drawing annotates as
carrying part of the deck load, and the **Promenade**.

**2. The control table moved.** The brief's §2 has been emptied and points at
[GEOMETRY-CONTROL.md](GEOMETRY-CONTROL.md). Two documents carrying `CTL-` rows is how a model drifts,
so `STT-007` fails the build if a control row ever reappears in the brief.

---

## The negative control

Three similar East River suspension bridges in one programme is the most likely route to a confident
wrong number, and this repository's brief was adapted from one of them — so the risk is structural,
not hypothetical.

The Manhattan and Williamsburg Bridges' figures are registered as **sources that may not be used**
(SRC-900, SRC-901). `STT-005` and `STT-006` scan every control **value**, in its declared unit,
against them — because the failure mode is a plausible number arriving without a label.

**The guard has already fired.** On its first run it caught three placeholders of this repository's
own: a 40 ft truss offset against Williamsburg's 40 ft truss depth, and a 120 ft tower width against
Manhattan's 120 ft deck width. Those placeholders were **moved rather than exempted** — a placeholder
is arbitrary by definition, so there is no cost to moving it, and an arbitrary value that happens to
look like a forbidden one blunts the guard.

---

## The three axes

Kept separate on purpose. Collapsing them hides the one that matters most — see
[CONFIDENCE-MODEL.md](CONFIDENCE-MODEL.md).

| Axis | Question | Example here |
|---|---|---|
| **Source confidence** `A`–`D` | How good is the evidence? | The main span is `A`: three sources, one a measured drawing |
| **Geometry provenance** `MEASURED`/`DOCUMENTED`/`INFERRED`/`ASSUMED` | How is the shape and position known? | The caissons are dimensioned to the foot and still only `INFERRED`, because which axis the 168 ft runs along is reasoned (OQ-005) |
| **Material** + its own grade | What is it made of, and how do we know? | Tower masonry is `A` — the drawing annotates the coursing. Deck surfacing is `D`, and that does **not** lower any deck part's geometry grade |

Provenance is **derived in the build, never hand-declared**, and `MEASURED` is computed rather than
hardcoded to zero, so the day a survey lands the number changes on its own.

**The cable sag shows the weakest-link rule doing real work.** The tower height is grade `A` at
276.5 ft, but the saddle drop below it and the minimum suspender length are both placeholders, so the
derived sag of 121.5 ft is grade `D`. Its ratio of 1:13.1 sits just outside the 1:7–1:12 band typical
of suspension bridges — which is *evidence the placeholder is wrong*. The model does not tune the
placeholder to make the ratio look respectable. It records the discrepancy, grades the cable `D`,
draws it dotted, and files OQ-001.

---

## Repository

```text
GEOMETRY-CONTROL.md      the single source of truth — every dimension, machine-parsed
SOURCE-REGISTER.md       every source, its read state, the negative controls, six conflicts
CONFIDENCE-MODEL.md      the three axes and the weakest-link rule
SCALE-HO.md              1:87.1 reporting scale
AGENT-INSTRUCTIONS.md    the build brief for this bridge
HOW-TO-DESIGN.md         the transferable method, carried over from manhattan-bridge-3d
scripts/                 build and validation pipeline — no script contains a dimension
tests/                   geometry regression (GRT-) + source traceability (STT-) suites
viewer/                  browser shell; viewer/public is the published surface
sources/drawings/        the retrieved HAER record and both Roebling reports
mesh/ cad/               generated artifacts, committed so a clean clone runs
```

Two pipeline rules that pay for themselves:

1. **Scripts contain no dimensions.** A number in Python is a bug.
2. **The control document is hashed into the build output**, and `GRT-001` fails when the parts
   manifest was built from a different hash. You will edit the document and forget to rebuild.

---

## Relationship to the rest of the programme

This module is a sibling of [manhattan-bridge-3d](https://github.com/Ethical-Tech-CoLab/manhattan-bridge-3d)
and [dumbo-district-3d](https://github.com/Ethical-Tech-CoLab/dumbo-district-3d), and follows the
contracts in [digital-3d-shared-contracts](https://github.com/Ethical-Tech-CoLab/digital-3d-shared-contracts).

`viewer/` is this module's own **inspect-mode shell**, which is the intended shape: the shared
`@d3d/viewer-kernel` is framework-agnostic decision logic, not a renderer, and the sibling bridge
viewer does not import it either. The canonical scene frame is carried here **byte-for-byte** and
hash-verified by `GRT-080`. The full module contract — manifest, asset registry, LOD ladder, level-2
proxy — is **not yet published**, deliberately, because OQ-008 leaves this module with no placement
it can defend. [viewer/README.md](viewer/README.md) sets out that boundary and the gap in full.

---

## What comes next

In priority order, from [GEOMETRY-CONTROL.md](GEOMETRY-CONTROL.md) §5:

1. **File the NYCDOT FOIL request.** Record, shop and rehabilitation drawings are not public. Longest
   lead time, largest payoff, retires more open questions than everything else combined.
2. Visit the **NYC Municipal Archives** at 52 Chambers Street. SRC-001 states plainly that the
   original drawings are there, and that this is *why* HAER prepared no historical report — a direct
   pointer to the primary record.
3. Read **Vogel 1983** directly, converting SRC-001's transmitted statistics table into an examined
   source, and settle OQ-011.
4. Locate **J. A. Roebling's 1867 design report** to retire OQ-001 and give the cables a real sag.

---

## Licence

Research content, control data and generated artifacts: **CC BY 4.0**. Code and viewer: **MIT**.
See [LICENSE.md](LICENSE.md).

> *Brooklyn Bridge Digital Twin: a source-governed control skeleton.* Ethical Tech CoLab, 2026.
