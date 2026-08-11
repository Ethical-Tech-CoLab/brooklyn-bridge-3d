# Open problems

What stands between this model and an accurate, convincing Brooklyn Bridge. Written after the
photo review and after indexing HAER NY-18's 77 plates, which changed the priorities materially.

The single most useful thing to understand first: **these problems are not all the same kind of
problem**, and treating them as one list is what sent a 272-photograph crowd campaign after
questions that photographs cannot answer.

| Class | What is wrong | What fixes it | Can a photograph help? |
|---|---|---|---|
| **A — wrong object** | The model builds a different thing from what is there | Modelling work, plus a few dimensions | **Yes** — it settles the kind |
| **B — right object, unknown size** | The shape is right, the number is invented | Drawings. Nothing else. | **No** — no scale in frame |
| **C — absent** | Real features not modelled at all | Modelling work | Yes, for form and existence |
| **D — systemic** | The method itself has a gap | Process change | n/a |

Ranked below by *impact per unit of effort*, not by severity.

---

## 1. The approach viaducts are the wrong kind of structure — class A

**Status: evidenced, buildable now, biggest single visual win.**

`CTL-110`/`111`/`112` draw the approaches as slender bents at 100 ft spacing — a placeholder chosen
only so the approaches reached the anchorages. [HAER NY-18-64](https://cdn.loc.gov/service/pnp/habshaer/ny/ny1200/ny1234/photos/120554pv.jpg)
is a near-square elevation of the real thing: a continuous **masonry arcade of pointed arches on
rectangular granite piers**, carrying a balustraded parapet, running unbroken to the tower.

This is roughly 3,000 ft of structure at each end — more length than the main span — and it is
currently the least truthful part of the model.

- **What the photograph gives**: the kind of object, the arch profile, the pier proportion, the
  parapet, and a *countable* number of bays over a known length. A count is an arrangement fact,
  not a dimension.
- **What it cannot give**: the bay spacing, pier width, arch span or rise as numbers.
- **Route**: derive bay spacing as *approach length ÷ counted bays*, publish it as grade `C`
  (derived from an image, per `CONFIDENCE-MODEL.md`) and label it plainly, **or** wait for the
  FOIL drawings and get `A`. The first is honest and available today; the second is better.

## 2. The tower tops are wrong where everyone looks — class A

**Status: evidenced, and deliberately *not* fixed. See `CONF-009`.**

The model cuts one open corridor across the tower top so all four cables ride saddles in a
continuous gap. [NY-18-41](https://cdn.loc.gov/service/pnp/habshaer/ny/ny1200/ny1234/photos/120531pv.jpg)
shows the truth: **each cable passes through its own tunnel in the granite**, masonry continuous
above it, onto a cast-iron saddle standing in an enclosed brick-vaulted chamber
([NY-18-40](https://cdn.loc.gov/service/pnp/habshaer/ny/ny1200/ny1234/photos/120530pv.jpg)).

You raised the cable attachment height once already and were right. This is the same area and the
same class of error, one level deeper.

It is *not* being fixed yet because the photographs give the arrangement and not one dimension of
it — opening width, chamber extent, saddle plinth height. Modelling it "about right" would replace
a **visible** error with an **invisible** one. It is registered as known-wrong and waits on drawings.

## 3. The stays radiate from a single invented node — class A

The model attaches all 16 stays at one point per tower.
[NY-18-38](https://cdn.loc.gov/service/pnp/habshaer/ny/ny1200/ny1234/photos/120528pv.jpg) — and the
photograph you sent — show them leaving the tower **across a spread of heights**, passing over the
cornice edge at intervals. The fan is the bridge's most recognisable silhouette after the arches,
and getting its origin wrong is visible from any distance.

Same shape of problem as #2: the arrangement is now evidenced; the spacing is not.

## 4. Nothing in this model is `MEASURED` — class D

0 measured · 11 documented · 93 inferred · 2 assumed. Every part's shape is reasoned from a
dimension, never observed. The honest ceiling on the current method is `INFERRED`.

Breaking that needs a survey product — LiDAR, photogrammetry, or a point cloud — which is the only
route to grade `C` geometry and the only thing that would let the model be *checked* rather than
argued about. Worth pursuing independently of FOIL.

## 5. Twelve placeholders that only drawings can retire — class B

| Control | Placeholder | What it distorts |
|---|---|---|
| `CTL-104`/`105` truss offsets | 38 ft / 15 ft | Deck cross-section; four trusses in the wrong lateral position |
| `CTL-108`/`109` tower plan at top | 42 × 116 ft | The taper — visible on every elevation |
| `CTL-103` deck structure depth | 3 ft | Deck thickness everywhere |
| `CTL-107` stair width | 12 ft | The DUMBO staircase |
| `CTL-110`–`112` approach supports | 100 / 8 / 10 ft | See #1 |
| `CTL-101` min suspender length | 3 ft | Midspan cable-to-deck relationship |
| `CTL-106` Brooklyn Curve drop | 15.9 ft | Where the promenade lands |

**None of these is answerable by any photograph, ever.** They are the FOIL request's payload.

## 6. `CONF-008` — the deck may be over-cambered — class B

SRC-002 annotates 110 ft clearance at the towers; scaling the same sheet gives 117 ft (Manhattan)
and 124 ft (Brooklyn). The explicit statement wins and the model uses 110 ft, but the same scaling
reproduces the drawing's stated 135 ft midspan clearance to within 1.1 ft, so it is not obviously
wrong. If the scaled reading is right, the deck's whole vertical profile is too steeply curved.
A single dimensioned section settles it.

## 7. Features not modelled at all — class C

Cheap, purely visual, and mostly evidenced already by the reviewed corpus and the HAER plates:

- **Railings and fencing** — 4 accepted photographs. Note they have *changed*: short lattice in
  older frames, tall mesh in recent ones. Model the current one and date it.
- **Lamp standards** — 6 accepted photographs; the cast fixture is clear in NY-18-44.
- **Cable bands and suspender sockets** — visible in NY-18-41 and NY-18-44.
- **Floor beams and stringers** — NY-18-46 shows the framing squarely.
- **Tower balconies / the promenade widening at the towers** — visible in several plates.

These add a great deal of visual credibility per hour and carry low risk, because none of them
supports a dimensional claim.

## 8. The method gap that caused the wasted campaign — class D

**A registered source was never fully read.** SRC-007 was marked read in Milestone 1 on the
strength of its data pages and measured drawing; its 77 photographs were never indexed. The crowd
campaign then went looking for exactly what NY-18-40, -41 and -64 already showed.

Fixed by [sources/haer-ny18-photo-index.json](sources/haer-ny18-photo-index.json), which indexes
all 77 with captions, LOC digital IDs and direct URLs — and by the rule now in `HOW-TO-DESIGN.md`:
**ask the sources you already hold before you ask the crowd.**

Still open: nothing yet *enforces* that a source marked read has been read in full. A register row
is one bit where the source is many documents.

---

## Order of work

1. **File the FOIL request** ([FOIL-REQUEST.md](FOIL-REQUEST.md)). It is the long pole — weeks of
   latency — and it unblocks #1, #2, #3, #5 and #6. File it before doing anything else.
2. **Class C visuals** (#7) while waiting. Low risk, high visible return, no dependency.
3. **Approach arcade** (#1) as counted-bay grade `C`, clearly labelled, so the worst-looking part of
   the model stops being wrong in kind.
4. **Tower tops and stays** (#2, #3) when the drawings arrive.
5. **Survey** (#4) as a separate, larger initiative.
