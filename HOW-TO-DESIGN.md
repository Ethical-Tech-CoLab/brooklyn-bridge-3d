# How to Design a Source-Governed Bridge Digital Twin

**Best practices for starting a new bridge model** — written for the Brooklyn Bridge and
Williamsburg Bridge efforts, but specific to neither.

This is the transferable method distilled from building
[manhattan-bridge-3d](https://github.com/Ethical-Tech-CoLab/manhattan-bridge-3d) through seven
milestones: the governance model, the tooling shape, the verified source landscape for all three
East River bridges, and — most usefully — the mistakes, with what each one cost.

> **This is not the same thing as `AGENT-INSTRUCTIONS.md`.** That file is a *repository-specific*
> build brief: what to build, for which bridge, in what order. This file is the *method* that
> outlives any one repository. A new bridge repo wants both — its own `AGENT-INSTRUCTIONS.md`
> naming its bridge and milestones, plus a copy of this document.

## Using this in a new repository

```powershell
# from the new repository root
Copy-Item ..\manhattan-bridge-3d\HOW-TO-DESIGN.md .\HOW-TO-DESIGN.md
```

Then write that repo's own `AGENT-INSTRUCTIONS.md` and work through the
[day one checklist](#14-day-one-checklist).

**Three scripts are worth porting as-is.** They are bridge-agnostic, dependency-free, and carry the
parsing contract that makes the governance rules enforceable rather than aspirational:

| From this repo | What it gives you |
|---|---|
| [scripts/control_model.py](scripts/control_model.py) | Parses the control document; rejects a graded row with no source, and a placeholder that cites one |
| [scripts/normalize_units.py](scripts/normalize_units.py) | The single unit-conversion implementation |
| [scripts/export_gltf.py](scripts/export_gltf.py) | glTF 2.0 / GLB writer with no third-party dependencies |

**What this guide will not do for you.** It carries the method and the traps, not the dimensions.
Every number in a new repository has to be sourced there from scratch — which is exactly why the
Manhattan Bridge's figures are registered in [SOURCE-REGISTER.md](SOURCE-REGISTER.md) as a
**negative control**. Three similar East River suspension bridges are the most likely way this
programme produces a confident wrong number.

---

## 1. The one rule

> **No dimension may exist in the model without tracing to a registered source with an explicit
> confidence grade. Anything unsourced is graded `D`, labelled a placeholder, and linked to a named
> open question.**

Everything else in this document is machinery for keeping that rule true when it becomes
inconvenient — which it will, roughly on day two, when you want the bridge to look right and the
sources will not tell you how deep the deck framing is.

The rule has a corollary that is easy to miss and does most of the work:

> **A model that admits it does not know something is more valuable than one that guesses well.**

A plausible guess is indistinguishable from a fact once it is in a GLB. That is the failure mode
this whole method exists to prevent.

---

## 2. What you are building

A browser-viewable 3D model of a bridge in which **every part carries its provenance**, so a reader
can ask of any surface: *how do you know that?* — and get a real answer, including "we do not".

Three artifacts, in dependency order:

1. **`GEOMETRY-CONTROL.md`** — the single source of truth. Every dimension, in machine-parsable
   tables. Scripts carry no numbers of their own.
2. **A build pipeline** that reads only that document and emits GLB + metadata.
3. **A viewer** that renders provenance into the geometry, not just into a side panel.

---

## 3. The three independent axes — the most important idea here

It is tempting to have one "confidence" number. Resist it. There are **three different questions**,
and collapsing them hides the one that matters most.

| Axis | Question | Where it lives |
|---|---|---|
| **Source confidence** `A`/`B`/`C`/`D` | How good is the evidence? | `SOURCE-REGISTER.md`, `CONFIDENCE-MODEL.md` |
| **Geometry provenance** `MEASURED`/`DOCUMENTED`/`INFERRED`/`ASSUMED` | How is the *shape and position* of this element known? | Derived per part in the build |
| **Material** + its own grade | What is it made of, and how do we know? | `GEOMETRY-CONTROL.md` material table |

**Why they must stay separate.** A source can be fully read, quoted and rated 5/5, and *still*
support only `ASSUMED` geometry — because a sentence establishing that an element exists says
nothing about where it is. The `manhattan-bridge-noise-dumbo` project's first implementation merged
these two and consequently labelled eight components "verified" on the strength of a source that
located none of them. That is recorded in its own `VISUAL-MODEL-FRAMEWORK.md` §5.4, and it is the
single most useful warning in this document.

Concretely, from the Manhattan Bridge model:

- The Brooklyn anchorage is **geometry grade B** (dimensions from good sources) and **material grade
  D** (no registered source says what it is built from). Every photograph shows stone. A photograph
  is not in the register, so it cannot grade a control.
- 56 parts are **source confidence D** but **provenance `INFERRED`**, not `ASSUMED` — their
  existence is documented, only their shape is reasoned. Merging the axes would have flattened all
  56 into the same bucket as the two parts that nothing documents at all.

**Do not fold a material grade into a geometry grade.** A grade-D material must not drag grade-A
geometry down; they answer different questions.

---

## 4. Geometry provenance, defined

Adopted from `VISUAL-MODEL-FRAMEWORK.md` §5.4 (Ethical Tech CoLab). Derive it in the build; never
hand-declare it.

| State | Meaning |
|---|---|
| `MEASURED` | Derived from an instrument reading of the actual structure. Carries a Level of Accuracy. |
| `DOCUMENTED` | *This element's own* position or dimension is stated numerically in a source that was read. |
| `INFERRED` | The element's **existence** is documented, but its position or dimension is reasoned. |
| `ASSUMED` | Placed by engineering judgement, with **no source statement locating it at all**. |

**The `INFERRED`/`ASSUMED` boundary is drawn on whether anything sourced speaks to the element**,
not on how confident you feel about its shape. Getting this wrong is easy: the first derivation
attempted on the Manhattan Bridge keyed off "depends on a placeholder control", which produced
`INFERRED = 0` — a binary that destroyed the very distinction the framework exists to carry. The
working rule:

```python
if "photogrammetry" in source_basis or "survey" in source_basis:  MEASURED
elif "control_dimension" not in source_basis or not sourced_refs: ASSUMED
elif placeholder_refs or "inferred" in source_basis:              INFERRED
else:                                                             DOCUMENTED
```

**Expect `MEASURED = 0` for a long time.** Compute it anyway rather than hardcoding zero, so the day
photogrammetry or survey lands, the number changes honestly.

---

## 5. Rendering rules — how to look good without lying

**The most important finding from the Manhattan Bridge work**, and the one that will save you the
most time:

> The best-looking provenance-tagged bridge schematics in this programme are **not built from
> measured drawings**. `VISUAL-MODEL-FRAMEWORK.md` states that **no element of either the Manhattan
> or the Williamsburg Bridge reaches `MEASURED` or `DOCUMENTED`.** Their visual quality comes
> entirely from *rendering discipline*.

So when someone says the model does not look convincing and blames missing schematics, that
diagnosis is usually wrong. Apply these first:

| State | Render |
|---|---|
| `MEASURED` / `DOCUMENTED` | Solid fill, solid outline, full opacity |
| `INFERRED` | Reduced opacity, **dashed** outline |
| `ASSUMED` | Low opacity, **dotted** outline, and excluded from every dimension callout |

Plus four interaction requirements:

- **The filter must hide, not fade.** "A faded outline is still a shape a reader will trace, and the
  honest experience of switching both off on this project is an empty frame."
- **Locus on selection.** Clicking an element shows the quoted passage its geometry rests on, or
  states that there is none.
- **A standing tally**, permanently on screen — not below the fold of a scrolling list, which is
  buried, which is what the framework warns against.
- **Materials drive appearance**, so stone reads as stone. Assign them in the control document, not
  in the renderer, and give the material table **no default rule** so an unmatched part is a build
  failure rather than a silent grey.

> **No dimension may be annotated on any element whose provenance is `ASSUMED`.** If we do not know
> where it is, we do not get to say how big it is.

**three.js note:** dashed lines need `computeLineDistances()` after building the geometry, or
`LineDashedMaterial` silently renders solid.

---

## 6. The control document

`GEOMETRY-CONTROL.md` holds every number. Machine-parsed, one row per control:

```
| Control ID | Key | Value | Unit | Source IDs | Confidence | Notes |
| CTL-002 | lower_level_abutment_to_abutment | 5790 | ft | SRC-000, SRC-001 | A | ... |
```

Enforce these in the parser, not in review:

- **Only grade `D` may cite no source.** Anything `A`/`B`/`C` without a source is a parse error.
- **Grade `D` may not cite sources.** A placeholder must not appear to rest on evidence.
- Values are bare decimals — no thousands separators, no ranges, no "approx".
- Units come from a closed set and are converted in exactly one place.

Separate tables for: control dimensions, **placeholders** (all grade `D`), derivation rules,
stations, elevations, open questions, materials, and provenance.

**Keep conflicts; do not resolve them silently.** The Manhattan model carries thirteen registered
conflicts between sources; seven are settled by weight of evidence and the rest stay open. A model
that hides source disagreement is lying by omission.

---

## 7. Pipeline shape

Dependency-free is a real advantage — anyone can rebuild without a toolchain hunt.

```
GEOMETRY-CONTROL.md
   └── control_model.py              parses controls, placeholders, materials; enforces the contract
        └── build_control_skeleton.py  derives stations/elevations, emits parts + GLB
             ├── export_gltf.py         hand-written glTF 2.0 / GLB writer, no dependencies
             ├── normalize_units.py     the ONLY unit conversion in the repo
             └── validate_dimensions.py runs the test suites
```

Two rules that pay for themselves repeatedly:

1. **Scripts contain no dimensions.** If a number appears in Python, it is a bug.
2. **Hash the control document into the build output**, and add a test that fails when the parts
   manifest was built from a different hash. You *will* edit the document and forget to rebuild.
   This caught it every single time.

---

## 8. The validation harness

Two suites: geometry regression (`GRT-`) and source traceability (`STT-`). Three modes:

- **`assert`** — fails the build.
- **`report`** — surfaces without blocking. Use for things that *should* change later, such as
  `MEASURED == 0`.
- **Ratchets** — e.g. "placeholder count has not regressed". Raising one requires editing the
  expectation *and writing the argument for it in the rationale field*.

**Give every guard teeth, and prove it.** After writing a test that asserts a defect is fixed, run
its measure against the *pre-fix* arrangement and confirm it fails there. A gap test that reported
`0` both before and after a fix would be worse than no test at all. Two minutes; has already caught
a vacuous test.

Useful invariants, learned the hard way:

- Every control reference on a part resolves to a real control ID.
- Every open question cited by a part exists in the open-questions table.
- Every part has a material rule, with no default.
- **No longitudinal gaps in the deck chain.** See [§11](#11-traps).

---

## 9. Milestone plan

Each milestone ends with a working artifact, not a document.

| # | Goal |
|---|---|
| 1 | Control skeleton + minimal viewer. Governance docs. Everything grade `D` is fine here. |
| 2 | Source verification. Retire placeholders by reading sources, not by guessing. |
| 3 | Period primaries examined **directly** — not via secondary citation. |
| 4 | Sourced detail geometry: towers, trusses, cables as real shapes. |
| 5 | Publish to the shared district contract (manifest, LOD ladder, proxy, frame). |
| 6 | Materials, provenance rendering, structural continuity. |
| 7+ | Photogrammetry, LOD switching, orthographic views. |

---

## 10. Source landscape for your bridge

**Verified by direct Library of Congress API query.** This is real intelligence; do not re-derive it.

| Bridge | HAER survey | Photographs | Measured drawings |
|---|---|---|---|
| **Brooklyn** | `ny1234` | 90 | **1 sheet** — "Plan, elevation, detail at Manhattan tower" |
| **Manhattan** | `ny0980` · HAER NY-164 | 11 + 1 colour | **none** |
| **Williamsburg** | `ny1263` · HAER NY-165 | 9 (Jet Lowe, 1991) | **none** |

**If you are building the Brooklyn Bridge, you are luckier than the other two teams.** That single
sheet is the only measured drawing of any East River bridge in the national record. Get it first, at
the highest available resolution. It alone can move a whole tower to grade `A`.

**If you are building the Williamsburg Bridge**, the one real transverse source is:

> Haight and Patel, *Reconstruction of the Williamsburg Bridge*, AISC, 2005 — co-authored by the
> NYCDOT Director of East River Bridges. Rubric 5/5.

It gives figure annotations naming the section components (`NORTH FOOTWALK`, `CL.TRK J1`,
`NEW BMT TRACKS`, `TRUSS BOTTOM CHORD`, …) and exactly **two** prose dimensions: the stiffening
truss is *"67 feet wide and approximately 40 feet deep and is pinned at each main tower."*

Two cautions on that paper, both important:

1. **Both dimensions describe the envelope and locate nothing inside it.** The truss members that
   carry them are therefore `INFERRED`, not `DOCUMENTED`. That is the difference between a drawing
   and a claim about a drawing.
2. **PDF text extraction does not preserve spatial order.** The label list is evidence that those
   components exist, *not* evidence of their left-to-right arrangement. Anything placed on extracted
   label order is `ASSUMED`.

**Other registered starting points:**

- **2017 NYC Topobathymetric LiDAR** — 1 ft DEM/DSM plus classified point cloud. On NYC Open Data,
  the NYS GIS clearinghouse, NOAA S3 `noaa-nos-coastal-lidar-pds`, and OpenTopography. Aerial, so it
  sees the **top of the deck** — the right tool for approach grade and ground profile, and useless
  for anything underneath.
- **NYC 3D Model by Community District** — buildings only, no bridge structure.
- **NYCDOT record, shop and rehabilitation drawings** — not public. **This is a FOIL request, not a
  research problem**, and it is the single highest-value action available on any of these bridges.
  File it in week one; it has a long lead time and retires more open questions than everything else
  combined.

**The negative control.** Register the *other* bridges' figures explicitly as sources that must
never enter your model. The Manhattan repo registers the Williamsburg 67 ft / 40 ft truss this way.
Cross-contamination between three similar East River suspension bridges is the most likely way this
programme produces a confident wrong number, and a named negative control turns that into a test
failure instead of a silent error.

---

## 11. Traps

Each of these cost real time on the Manhattan Bridge.

**A sourced count with no geometry is a silent hole.** *(Contributed by `brooklyn-bridge-3d`.)* A
reviewer said the main cables looked like they attached well below the tower tops. The saddle
elevation was in fact right. The cause was that a grade-`A` control — "eight cast iron saddle
bearings" — had been registered at Milestone 1 and **never modelled**, so the cable ran into a solid
masonry block and disappeared some 25 ft before reaching its true high point. Nothing failed, because
every test asked whether the geometry that existed was sourced, and none asked whether the sources
that existed had geometry. **Add a test that named structural counts are referenced by at least one
part, and a report-only census of sourced controls no part uses.** The census found a second instance
on its first run.

**Trusting a measurement whose own sanity check had already failed.** The same saddle figure was
first measured at 16.5 ft from a pass whose isotropy check came out at 1.73 on a drawing that must be
1.00. That should have stopped the measurement being used at all. It had latched onto a flagstaff
instead of the masonry cap. **When you scale a drawing, measure a ratio rather than an absolute** —
it is immune to scale error — **and validate the chain against a figure that played no part in
setting it.** Reproducing the drawing's own stated 135 ft clearance to 1.1 ft is what finally made
the second measurement trustworthy.

**Geometry stopping where the model stopped, not where the bridge stops.** All deck geometry ended
at the anchorage face because that is where the *suspended* structure ends — leaving the roadway and
all four tracks terminating in mid-air and contradicting a grade-`A` control that described the
lower level as continuous abutment to abutment. Two separate versions of this bug shipped. **Write a
test that asserts no longitudinal gap in the deck chain**, from the first milestone.

**Inventing coordinates and then using them as ground truth.** Plausible-looking tower latitudes and
longitudes were nearly used to "verify" a placement. They implied 823 m between towers against a
sourced main span of ~448 m. If a coordinate is not in the register it cannot verify anything —
including your own work.

**Sub-agents conflating your repo with the outside world.** An exploration agent with filesystem
access read the local repository and reported its own `CTL-` and `SRC-` values back as *external
corroboration*. Always ask where a fact came from, and check.

**Truncating a source and building on the fragment.** A tower description was cut short; the full
passage gave four box-section legs tapering 32 ft → 10 ft standing in the planes of the four
trusses — a materially different tower. Read the whole passage before modelling from it.

**Trusting a secondary citation's gloss.** A primary said the towers are "of steel 330 feet high"; a
secondary rendered that as 330 ft *to the tops of the cables*. Different claim, different geometry.
Examine primaries directly and quote them.

**Arithmetic beating an explicit statement.** A pier capstone height was derived at 31 ft; a period
primary stated 23 ft. The explicit statement wins, and the disagreement is registered as a conflict
rather than smoothed away.

**A validator with a parsing bug reporting success.** A "verified" column parser choked on markdown
bold (`**yes**`), so every verified source read as unverified. **Test your tests.**

**A document that hashes two different ways.** If you hash your control document into build
outputs -- and you should -- add a `.gitattributes` forcing `text eol=lf` on day one. Without it
Git's `autocrlf` gives a Windows checkout CRLF while the committed blob and every Linux CI runner
keep LF, so the same content produces two different provenance hashes and a local build disagrees
with CI for a reason that has nothing to do with geometry. Mark binaries (`*.glb`, `*.jpg`, `*.png`,
`*.pdf`) explicitly, or line-ending conversion will corrupt them.

**Writing into the repo by accident.** A `curl -o` loop with relative paths overwrote `README.md`.
Use absolute output paths.

**Browser and tooling gotchas.** Headless test pages may never fire `requestAnimationFrame` or
`ResizeObserver`, so a canvas resize driven only by those cannot be verified there — drive layout
changes from an explicit token as well. Set a viewport explicitly or screenshots fail with zero
width. Detach long-running dev servers or they die with the session.

**A field that cannot express "I don't know" launders ignorance rather than preventing it.** The
value still gets written; it just stops being marked as a guess. A photo-survey contract required a
camera position and a full RFC3339 timestamp — reasonable for a volunteer with a phone, impossible
for an archival plate. The harvester complied by truncating free text to ten characters and
declaring day precision on all 272 records, so `captured_at: "Taken on 2"` shipped wearing a
confident precision badge. Make absence expressible, then make it *declared*: a position may now be
omitted only when `position_source` says `unknown`, and a date may be as short as `1898`, with the
stated precision cross-checked against the string. Same rule as grade `D` — the honest answer must
have somewhere to go.

**A version declared is not a version checked.** A published document claimed
`contract_version: 1.0.0` and violated the contract six ways: invented field names, wrong types,
fields a strict definition forbids. Nobody had lied; the tooling simply never asked, because
declaring conformance costs nothing and validating it takes a command. If you write a document
against a schema, validate it in CI on the way out — otherwise the version string is decoration.

**A code path that only runs after a human acts is a code path that has never run.** Half of those
violations lived in the branch that executes when a reviewer accepts a photograph, which stayed
dormant through an entire campaign. Feed the tool a synthetic decision file and make the branch run
once before you ship it; the first execution found an empty required array within seconds.

**Crowd-sourced photography is biased toward the view worth photographing, which is systematically
not the view your model is missing.** A campaign of 272 licence-checked images produced a decisive
answer on the promenade decking and the roadway surface — both photographed constantly — and
returned *zero* frames of the approach arcade and zero of the staircase, which were the two
categories it was built to close. People shoot the bridge from the promenade and the waterfront,
not the viaduct they drive under. Plan for this: put the categories you actually need in the
campaign so the gap is measured rather than assumed, and treat an empty category as a finding worth
recording. It tells you to go and get the drawings instead of harvesting more.

**Ask the sources you already hold before you ask the crowd.** The campaign above was, in the end,
unnecessary for its two headline questions. A registered source — an archival photographic survey —
contained a square elevation of the approach arcade and two interior views of the cable saddles and
their masonry openings. It had been marked *read* in the register on the strength of its written
data pages and its one measured drawing; nobody had indexed its 77 photographs. A source is not a
document, it is a **collection**, and "read" is one bit describing many. Before commissioning any
new evidence-gathering, index every registered source at the level of individual sheets and plates,
and publish that index. It is a day's work that can save a fortnight's.

**A placeholder inherited from one kind of structure can be impossible for another.** When the
approach viaducts were rebuilt from bents into the masonry arcade the photographs showed, the bent
spacing carried straight over — and a two-centred pointed arch needs a rise of at least half its
clear span, so the inherited 100 ft bay drove arch crowns clean through the deck soffit. The number
had been harmless for years because nothing built from it could contradict it. **A placeholder is
only as safe as the geometry that consumes it**, so when you change what consumes one, add the
realisability check at the same time. Note also that this is a one-sided constraint: an arch below
that ratio does not exist at any tolerance, so it needs its own `at_least` check rather than an
equality with a fudge factor.

**Fixing the kind is not the same as fixing the accuracy, and it is worth saying which you did.**
The rebuilt arcade contains not one sourced dimension — it is graded `ASSUMED`/`D` throughout, as
the bents were. It is not more accurate. It is more *truthful*, because a reviewer now sees the
right species of object with the same honest labelling. Conflating the two is how a model starts
looking more authoritative than it is.

**Re-arm a guard when the world changes underneath it.** A guard forbidding citation of an
unreviewed photo corpus stopped being able to fail the moment the corpus was reviewed — the
injected defect had become a legitimate act. Nothing alerted us except a defect-injection harness
that reported the guard as vacuous. A guard that cannot fail is worse than no guard, because the
roster still counts it. If you assert that your guards have teeth, assert it every build.

**A photograph is evidence about the day it was taken, and your corpus is not from one day.** A
harvested set spanned 1867 to 2026, and the model is of the structure as it stands. Those are only
compatible if archival frames are kept away from claims they cannot support: the granite is
original fabric so an 1876 photograph still evidences it, while the roadway surface is renewed on a
maintenance cycle so a Victorian photograph evidences something that no longer exists. Declare each
subject `renewed` or `stable` and refuse old photography for the renewed ones. The human reviewer
here got it right unprompted — tagging every pre-1920 frame as context only — which is precisely
why it needed encoding: correctness that depends on one person's instinct is not yet a property of
the system.

**Ambiguity is a legitimate parse result.** EXIF and archive captions emit `04/17/24`, and the
day/month order is only recoverable when one field exceeds 12. Given `04/05/24`, guessing a
convention is wrong roughly half the time while looking exactly as confident as a correct answer;
degrading to `2024` at year precision is right every time. Prefer a coarser true answer to a
precise coin-flip — and note that this only became visible because a *different* guard demanded a
date the parser had silently failed to produce.

---

## 12. Shared contract integration

If a district or neighbourhood twin will consume your bridge, publish a module contract early — it
is cheap and it surfaces coordinate-frame disagreements while they are still theoretical.

- Serve `viewer/public/` at your site root; the manifest is the entry point.
- **Copy the canonical frame byte-for-byte** and verify by hash. Do not re-serialise it, and do not
  edit the anchor.
- Use **document-relative URLs** so one manifest works both co-served and standalone, and assert
  both layouts in a test.
- **Declare your vertical datum**; do not silently convert. Author against whatever your sources
  use — the conversion belongs at placement time.
- Ship a **level-2 proxy** (a few thousand triangles) early. That is what a pedestrian actually
  sees, and it makes the integration real long before the detailed model is ready.
- **Audit any placement a consumer proposes for you, then ratify it in your own words.** Reproduce
  their numbers, test an alternative estimator, and find an independent cross-check. On the
  Manhattan Bridge the ASCE landmark plaque coordinate — which played no part in deriving the
  placement — landed 10.5 m from the proposed origin, which justified raising it from grade D to C.

---

## 13. Repository structure

```text
GEOMETRY-CONTROL.md      the single source of truth
SOURCE-REGISTER.md       every source, with verification state and conflicts
CONFIDENCE-MODEL.md      what A/B/C/D mean and how a part inherits its grade
SCALE-HO.md              display-scale reference, if modelling for a physical scale
AGENT-INSTRUCTIONS.md    the build brief for THIS bridge: scope, milestones, deliverables
HOW-TO-DESIGN.md         this file: the transferable method, copied in from a sibling repo
scripts/                 build and validation pipeline
tests/                   geometry regression + source traceability suites
viewer/                  browser viewer; viewer/public is the published contract surface
mesh/  cad/              generated artifacts
sources/                 retrieved source material and licences
photogrammetry/          capture inputs, when they exist
```

---

## 14. Day one checklist

1. Copy this file in as `HOW-TO-DESIGN.md`, and write a separate `AGENT-INSTRUCTIONS.md` naming
   your bridge, its scope and its milestones. Keep the two distinct: method here, brief there.
2. Create `SOURCE-REGISTER.md`. **Register the other two bridges as negative controls immediately.**
3. Create `CONFIDENCE-MODEL.md` — define `A`/`B`/`C`/`D` and the weakest-link inheritance rule.
4. Create `GEOMETRY-CONTROL.md` with the table skeletons from §6. It is fine for every row to be
   grade `D` on day one; it is not fine for a row to have no grade.
5. Port `control_model.py`, `normalize_units.py` and `export_gltf.py` from the Manhattan repo — they
   are bridge-agnostic and dependency-free.
6. Write the control-document-hash test **before** the second milestone.
7. Write the deck-continuity test **before** you model any deck.
8. **File the NYCDOT FOIL request.** Longest lead time, largest payoff.
9. Build the skeleton, stand up the viewer, and only then start arguing about geometry.

---

## 15. What good looks like

At the end of the Manhattan Bridge's seventh milestone:

- 95 parts, 72 controls, 21 sources, 20 open questions, 13 registered conflicts
- Provenance: 0 measured · 37 documented · 56 inferred · 2 assumed
- 74 tests passing, 5 report-only, 0 failing
- Turning off `inferred` and `assumed` in the viewer leaves the towers, the anchorages and the
  station markers — and **that emptiness is the honest picture**, published rather than hidden

Aim for that. A small model that can defend every line is worth more than a detailed one that
cannot.
