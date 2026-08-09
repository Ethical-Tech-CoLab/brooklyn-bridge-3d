# Confidence Model

Three independent axes. **Do not collapse them into one number** — that is the mistake this document
exists to prevent, and it has already been made once inside this programme.

| Axis | Question it answers | Where it is declared |
|---|---|---|
| **Source confidence** `A` `B` `C` `D` | How good is the evidence? | [SOURCE-REGISTER.md](SOURCE-REGISTER.md) and each row of [GEOMETRY-CONTROL.md](GEOMETRY-CONTROL.md) |
| **Geometry provenance** `MEASURED` `DOCUMENTED` `INFERRED` `ASSUMED` | How is the *shape and position* of this element known? | Derived per part by `scripts/build_control_skeleton.py`. Never hand-declared. |
| **Material** and its own grade | What is it made of, and how do we know? | The material table, [GEOMETRY-CONTROL.md](GEOMETRY-CONTROL.md) §7 |

Why they must stay separate: a source can be fully read, quoted, and rated `A`, and *still* support
only `ASSUMED` geometry — because a sentence establishing that an element **exists** says nothing
about **where it is**. A sibling project merged these two axes and consequently labelled eight
components "verified" on the strength of a source that located none of them.

**A grade-`D` material must not drag grade-`A` geometry down.** They answer different questions. The
Brooklyn Bridge towers are geometry grade `A` and material grade `A` (SRC-002 annotates the stone
coursing directly); the approach viaducts are geometry grade `D` and material grade `D`.

---

## 1. Source confidence

| Grade | Meaning | Example in this repository |
|---|---|---|
| `A` | Stated numerically in an official record, an archival measured drawing, or a period primary that was **opened and read here**. | Main span 1595.5 ft — SRC-001, SRC-002 and SRC-003 all state it; SRC-002 is a measured drawing. |
| `B` | Derived from consistent statements across multiple read sources, or from one read source plus control geometry, without any single source stating the number. | Suspender longitudinal pitch — the count is grade `A`, the even distribution is reasoning. |
| `C` | Derived from an existing mesh, photogrammetry, or a coordinate aligned to controls. | None yet. Expect the LiDAR and the HAER photographs to land here. |
| `D` | **Placeholder.** Inferred, decorative, or a shape hint. No source states it. | Cable sag at midspan — no read source gives it, so it rests on two `D` placeholders. |

Two rules the parser enforces, not the reviewer:

- **Only grade `D` may cite no source.** An `A`/`B`/`C` row with an empty source cell is a parse error.
- **Grade `D` may not cite sources.** A placeholder must not appear to rest on evidence.

### Inheritance — weakest link

A derived value takes the **lowest** grade among its inputs.

```text
main_span (A) + side_span_each (A)          -> anchorage station (A)
clearance (A) + truss_depth (A)             -> truss top elevation (A)
truss_top (A) + min_suspender_length (D)    -> cable elevation at midspan (D)
```

The third line is the important one. The cable's midspan elevation is arithmetic on two numbers, one
of which nothing supports — so the whole result is `D`, and the sag figure printed in the build
report is `D`, and the viewer draws that cable with a dotted outline. The arithmetic being sound does
not launder the input.

---

## 2. Geometry provenance

Adopted from `VISUAL-MODEL-FRAMEWORK.md` §5.4 (Ethical Tech CoLab). **Derived in the build, never
hand-declared.**

| State | Meaning |
|---|---|
| `MEASURED` | Derived from an instrument reading of the actual structure. Carries a Level of Accuracy. |
| `DOCUMENTED` | *This element's own* position or dimension is stated numerically in a source that was read. |
| `INFERRED` | The element's **existence** is documented, but its position or dimension is reasoned. |
| `ASSUMED` | Placed by engineering judgement, with **no source statement locating it at all**. |

The `INFERRED`/`ASSUMED` boundary is drawn on **whether anything sourced speaks to the element** —
not on how confident the author feels about the shape.

The derivation, in `scripts/build_control_skeleton.py`:

```python
if "photogrammetry" in source_basis or "survey" in source_basis:   MEASURED
elif "control_dimension" not in source_basis or not sourced_refs:  ASSUMED
elif placeholder_refs or "inferred" in source_basis:               INFERRED
else:                                                              DOCUMENTED
```

**`MEASURED` is expected to be 0 for a long time.** It is computed rather than hardcoded, so that on
the day a survey or photogrammetry set lands, the number changes honestly. Test `GRT-020` reports
this count without failing the build.

---

## 3. How provenance is rendered

Provenance is drawn **into the geometry**, not only into a side panel.

| State | Render |
|---|---|
| `MEASURED` / `DOCUMENTED` | Solid fill, solid outline, full opacity |
| `INFERRED` | Reduced opacity, **dashed** outline |
| `ASSUMED` | Low opacity, **dotted** outline, and excluded from every dimension callout |

Four interaction rules go with it:

1. **The filter hides; it does not fade.** A faded outline is still a shape a reader will trace.
   Switching `INFERRED` and `ASSUMED` off must be capable of leaving an almost empty frame — and if
   it does, that emptiness is the honest picture and gets published rather than hidden.
2. **Locus on selection.** Selecting a part shows the control rows its geometry rests on, or says
   plainly that there are none.
3. **A standing tally**, permanently on screen, not below the fold of a scrolling list.
4. **Materials drive appearance**, assigned in the control document rather than in the renderer, and
   the material table has **no default rule** — an unmatched part is a build failure, not a silent grey.

> **No dimension may be annotated on any element whose provenance is `ASSUMED`.** If we do not know
> where it is, we do not get to say how big it is.

---

## 4. Required metadata

No part enters the model without all of:

```text
part_id
system / subsystem
source_basis            list: control_dimension | placeholder | drawing | photo | inferred | survey
control_refs            control IDs this part's geometry depends on
confidence              A | B | C | D   (weakest link over control_refs)
provenance              MEASURED | DOCUMENTED | INFERRED | ASSUMED   (derived, never declared)
material                from the material table; no default
open_questions          OQ IDs, where the part depends on something unresolved
prototype_units         meters
ho_scale_units          millimetres
review_status
last_modified_by_agent
```

Every one of these is asserted by the test suites. A part missing any field fails the build.
