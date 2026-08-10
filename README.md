# Brooklyn Bridge Digital Twin

**▶ [View the model in your browser](https://ethical-tech-colab.github.io/brooklyn-bridge-3d/)**

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
| Controls | **99** — 87 sourced (83 grade `A`, 4 grade `B`), 12 placeholders |
| Sources read | **13 registered and read**, plus 4 registered as linked-only or negative controls |
| Parts | **106** across 8 systems |
| Provenance | 0 measured · 11 documented · 93 inferred · 2 assumed |
| Tests | **45** — 40 asserting, 5 report-only, **0 failing** |
| Guards proven | 13 injected defects, each confirmed to fail its guard |
| Cross-source checks | 8, all closing |
| Registered conflicts | 8 — five settled with reasoning, three left open |
| Open questions | 17 — one closed, one answered, two half-answered |

Turning `INFERRED` and `ASSUMED` off in the viewer leaves the two anchorages and the seven station
markers. **That emptiness is the honest picture of what these sources actually locate**, and it is
published rather than hidden.

---

## How to review this model

**The published viewer is at
[ethical-tech-colab.github.io/brooklyn-bridge-3d](https://ethical-tech-colab.github.io/brooklyn-bridge-3d/)**
— nothing to install. It is rebuilt and revalidated on every push to `main`, and the workflow fails
rather than deploying if the committed artifacts do not match a fresh build.

To run it locally instead:

```powershell
cd viewer; npm install; npm run dev      # http://localhost:5174
```

Orbit-drag, scroll to zoom, right-drag to pan. Click any part and the right panel lists the control
rows its geometry rests on, with values, grades and source IDs — or says plainly that there are none.
The toolbar button swaps to HO 1:87.1 and re-reports every extent in millimetres. Give the window
some width; below about 1100 px the side rails stack under the viewport.

**Do this first: untick `INFERRED` and `ASSUMED`.** The bridge nearly vanishes. Everything that
disappears is something reasoned rather than read, which makes it the fastest way to find where this
model is bluffing.

**Then open the Compare panel.** Eight reference views ship with the model — the HAER measured
drawing's elevation, plan and tower detail, and five HAER photographs, all works of the U.S.
Government. Pick one and the camera flies to its viewpoint; then **Overlay** puts it over the model
with opacity, scale and offset controls, or **Side by side** splits the frame with a draggable
divider. The overlay constrains the 3D view to the image's own aspect ratio, so a scaled orthographic
drawing actually lines up instead of merely sitting on top.

Copyrighted galleries — HistoricBridges.org's detail photography, Historic-Structures.com's history —
appear under **"Linked, not copied"**. They informed the model; they are not served from the site.

**Where the model is weakest — aim here rather than at the parts that are already defensible:**

| What | Why it deserves attack |
|---|---|
| **The approach supports are the wrong kind of object** | Not merely the wrong size. SRC-004 describes brick piers and arches and HistoricBridges' photography shows a masonry arcade; the model draws slender bents because nothing dimensions the arcade. The only two `ASSUMED` parts in the model. OQ-007. |
| **Truss and cable transverse spacing** | CTL-104/105 put them at 38 ft and 15 ft off centreline, bounded only by the 85 ft deck. Sight down the bridge axis: this is the weakest visible geometry. OQ-002. |
| **Towers above the waterline** | The 59 × 140 ft plan is grade `A` *only at mean high water*. The taper to the top is invented, which is why `tower_*_shaft` is grade `D` in an otherwise grade-`A` system. OQ-004. |
| **Caisson orientation** | 168/172 × 102 ft is solidly sourced, but *which axis is which* is reasoning. Rotated 90° the foundations are wrong, and no current test would catch it. OQ-005. |
| **The Brooklyn Curve is drawn straight** | Its 910 ft length and 11 ft width are grade `A`, but NYCDOT calls it a *curve* and the model has no radius for it. A registered omission — OQ-014. |
| **The deck is one envelope** | Five vehicle lanes and a protected bike lane are sourced as *facts*, but nothing registered gives their transverse positions. OQ-003. |
| **The deck may be over-cambered** | CTL-011's annotated 110 ft at the towers is used, but scaling the same drawing gives 117 ft at Manhattan and 124 ft at Brooklyn — so the model's rise to midspan may be about twice the real one, and the two towers are not actually alike. Registered as CONF-008 / OQ-017 rather than quietly adjusted. |
| **The tower cornice opening is reasoned** | That the masonry above the saddle cannot be solid across the cable lines follows from a grade-`A` statement; *how wide* the opening is does not. OQ-016. |

**Other ways in.** Drag `mesh/glb/control_skeleton.glb` onto any glTF viewer for pure shape critique
without the metadata. Read [SOURCE-REGISTER.md](SOURCE-REGISTER.md) for the conflicts — most are
settled with reasoning you are invited to dispute. And check the sources directly: the HAER measured
drawing and both Roebling reports are committed under [sources/drawings/](sources/drawings), so every
grade `A` number can be traced back to the sheet it came off.

---

## Help close the open questions — the photo review

**[Open the review sheet](https://ethical-tech-colab.github.io/brooklyn-bridge-3d/review/index.html)**
— 272 openly-licensed photographs, no install, works on a phone.

Every placeholder still standing in this model is a question about **what something is made of** or
**how it is arranged** — not a dimensional gap that a better drawing would fill. The deck and
promenade surfaces are graded `D` because no registered source says what they are. The approach
supports are the wrong *kind* of object. Nobody has established how the masonry above the saddle is
arranged. A person looking at photographs settles all three; re-reading the 1877 report settles none
of them.

So: tick every category a photograph can actually inform, `skip` the rest, press **Save**, and drop
the downloaded `review-decisions.json` into [sources/photos/](sources/photos). The legend names the
open question behind each category, so a tick answers something specific.

Two limits, enforced rather than merely stated:

- **A photograph cannot carry a dimension.** Without scale control in the frame it cannot measure.
  The category vocabulary's closed grant set is `material · arrangement · existence · condition ·
  appearance`, and `dimension` is deliberately not in it.
- **Nothing is evidence until someone looks.** All 272 records are `auto_screened` today, so SRC-018
  grades nothing, and `STT-017` fails the build if any control or material rule cites it before a
  single photograph has been accepted.

Built with the shared [`tools/photo-survey/`](https://github.com/Ethical-Tech-CoLab/digital-3d-shared-contracts/tree/main/tools/photo-survey)
pipeline, so any structure in this programme can run the same campaign.

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

**The walkway is not the roadway, and the model was wrong about that.** NYC DOT's own 2016
*Brooklyn Bridge Promenade* study divides the promenade into eight named sections and dimensions
every one of them. The last is the **Brooklyn Curve**: 910 ft, 11 ft wide, annotated *"excess space
on north side of fence to accommodate staircase."* That is the section carrying the walkway past
Adams Street where the roadway ends, and it holds the stair tourists use to reach DUMBO — down to
Washington Street and Prospect Street, by Cadman Plaza East.

The first build ended the walkway with the road, which also left that staircase attached to nothing.
`GRT-034` now asserts the overhang equals the sourced curve length, and the model reports it at
910.0 ft.

That study also produced two more cross-source checks, and both close:

| Check | Residual |
|---|---|
| NYCDOT's six on-structure promenade typologies vs HAER's bridge proper length | −77.5 ft on 3455.5 ft, **2.2%** — a 2016 pedestrian study against a measured drawing of an 1883 structure, neither derived from the other |
| NYCDOT's promenade passage through one tower vs HAER's tower thickness at mean high water | −4.5 ft, and **narrower**, which is the direction the taper predicts since the walkway crosses well above the waterline |

**A conflict resolved by arithmetic, not preference.** HAER's data pages give the tower height as
`276.6 ft`; the measured drawing says `276'-6"` and ASCE says `276.5`. HAER decimalises its other
feet-and-inches values correctly — 44'-6" → 44.5, 78'-6" → 78.5, 33'-9" → 33.8 — so its `276.6` is a
digit error. The model uses 276.5, records 276.6 as CTL-021, and `GRT-061` fails if the recorded
figure ever reaches the geometry.

All six conflicts, including the two that remain open, are in [SOURCE-REGISTER.md](SOURCE-REGISTER.md).

**A correction the model made to its own critic.** An earlier version of this README called the
derived cable sag wrong, on the grounds that its ratio fell outside the 1:7 to 1:12 band typical of
suspension bridges. That reasoning was itself the error: the band describes a *pure* suspension
bridge, and this one is not — its diagonal stays are a second load path, which is the defining
feature of the Roebling system and which lets the cable run shallower.

Scaling the measured drawing settled it. SRC-002 is orthographic with a dimensioned 1595.5 ft main
span, and the same scale independently reproduces the drawing's own stated 135 ft midspan clearance
to within 1.1 ft — a figure that played no part in setting it. Measured that way the saddle sits
**14.5 ft below the tower top**, which had been a 0 ft placeholder, and the sag is about 110 ft
against the model's 107 ft. CTL-064 now carries that at grade `B`: the drawing is grade-`A` material,
but the *scaling* is this repository's own derivation and a line on that sheet is 5 ft thick.

**A second correction, from a reader looking at the render.** The cables appeared to attach well
below the tower tops — "meters lower", which is what a viewer saw and the arithmetic denied. Both
were right. The saddle elevation was sound, but **CTL-046 — eight cast iron saddle bearings, grade
`A` — was registered and never modelled**, so the cable simply ran into a solid masonry block and
disappeared some 25 ft below the top, well before reaching its true high point.

The fix was geometry, not a number. The tower is now a shaft up to the saddle plus a cornice above
it, and the cornice is modelled as two masses outboard of the outer cables rather than a solid slab —
because SRC-002 states the cables were "CARRIED **THROUGH** THE TOWERS ON EIGHT CAST IRON SADDLE
BEARINGS", so the masonry at that level cannot be continuous across them. The saddles themselves are
now built, sized from the sourced cable diameter so no new placeholder was needed.

`STT-015` now fails the build if any counted structural element is registered and never modelled. It
found a second instance immediately: the anchorages were not citing their own count control.

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
