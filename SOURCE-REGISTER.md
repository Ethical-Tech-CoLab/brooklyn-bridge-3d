# Source Register

Every dimension in this repository traces to a row in this table. A source that has not been
**opened and read** may be registered, but it may not be cited by a control.

**Read state** is deliberately separate from confidence. `read` means the document was retrieved and
its relevant passages were examined in this repository's own work — not that a secondary source
quoted it. `registered` means we know it exists and have not yet opened it; such a source appears
only in the [verification queue](#verification-queue).

---

## Register

| Source ID | Title | URL or archive ref | Type | Licence | Read state | Confidence impact | Notes |
|---|---|---|---|---|---|---|---|
| SRC-001 | HAER No. NY-18, *Brooklyn Bridge* — data pages (8 pp.) | [loc.gov/pictures/item/ny1234](https://www.loc.gov/pictures/item/ny1234/) · local: [sources/drawings/haer-ny18-data-pages.pdf](sources/drawings/haer-ny18-data-pages.pdf) | Archival engineering record | U.S. Government work, no known restrictions | **read** | A | Carries the "Bridge's Vital Statistics" table. That table is itself credited to Robert M. Vogel, *Building Brooklyn Bridge: The Design and Construction, 1867–1883* (Smithsonian, 1983), so it is a **secondary transmission of a secondary source** — high quality, but not a period primary. Treated as grade A only where a second source agrees. |
| SRC-002 | HAER No. NY-18, measured drawing, sheet 1 of 1: *Plan, elevation, detail at Manhattan tower*; delineator Paul Berry | [loc.gov/pictures/item/ny1234.sheet.00001a](https://www.loc.gov/pictures/item/ny1234.sheet.00001a/) · local: [sources/drawings/haer-ny18-sheet-01.tif](sources/drawings/haer-ny18-sheet-01.tif) | **Measured drawing** | U.S. Government work, no known restrictions | **read** (14484 × 9632 px, read by crop at full resolution) | A | **The only measured drawing of any East River suspension bridge in the national record.** Explicitly datumed to mean high water. Supplies the span chain, the tower elevation and plan extents, the arch geometry, and the two approach lengths. |
| SRC-003 | ASCE Historic Civil Engineering Landmark — Brooklyn Bridge | [asce.org/…/brooklyn-bridge](https://www.asce.org/about-civil-engineering/history-and-heritage/historic-landmarks/brooklyn-bridge) | Engineering society reference | © ASCE, quoted for citation | **read** | A/B | Short fact list. Confirms main span and tower height; quotes John Roebling's 1854 proposal on the six lines of trusses; describes the original deck arrangement. |
| SRC-004 | Washington A. Roebling, *Report of the Chief Engineer of the New York & Brooklyn Bridge*, January 1, 1877 | [archive.org/details/reportofchiefeng00roeb](https://archive.org/details/reportofchiefeng00roeb) · local: [sources/drawings/roebling-1877-chief-engineer-report.txt](sources/drawings/roebling-1877-chief-engineer-report.txt) | **Period primary** | Public domain | **read** (full OCR text, 308 kB) | A | The builder's own report. Supplies the New York anchorage in full plan and elevation, the tower arch geometry, the saddle detail, and the 1876 wire specification. OCR damage is present and is called out wherever it touches a cited passage. |
| SRC-005 | Washington A. Roebling, *Pneumatic Tower Foundations of the East River Suspension Bridge*, 1873 | [archive.org/details/pneumatictowerfo00roeb](https://archive.org/details/pneumatictowerfo00roeb) · local: [sources/drawings/roebling-1873-pneumatic-tower-foundations.txt](sources/drawings/roebling-1873-pneumatic-tower-foundations.txt) | **Period primary** | Public domain | **read** (full OCR text) | A | The caisson monograph. Supplies both caisson footprints, the air-chamber height and the roof thickness, with an internal arithmetic check on the areas. |
| SRC-006 | HAER No. NY-18, index to photographs / caption pages (9 pp.) | local: [sources/drawings/haer-ny18-caption-pages.pdf](sources/drawings/haer-ny18-caption-pages.pdf) | Archival photo index | U.S. Government work | **read** | — | 73 photographs in seven groups: aerials, ground views, towers, suspension system, superstructure, anchorages and approaches, Promenade. **No dimensions.** Registered so that a later milestone can address individual photographs by number. |
| SRC-007 | HAER No. NY-18 photographs (77 b/w, 8 colour transparencies) | [loc.gov/pictures/collection/hh/item/ny1234](https://www.loc.gov/pictures/collection/hh/item/ny1234/) | Archival photographs | U.S. Government work | registered (catalogue read, images not yet retrieved) | B (future) | Tier B detail geometry for Milestone 4. Cannot grade a control until individual plates are examined. |
| SRC-008 | Library of Congress catalogue record for HAER NY-18 (survey `ny1234`) | [loc.gov/pictures/item/ny1234](https://www.loc.gov/pictures/item/ny1234/) | Catalogue metadata | U.S. Government work | **read** | C | Gives call number HAER NY,31-NEYO,90-, NRHP 66000523, and a latitude/longitude of 40.709109, −74.000695. **That coordinate locates the record, not any structural element**, so it may not verify a placement. See OQ-008. |
| SRC-010 | `digital-3d-shared-contracts` — canonical scene frame `nyc-harbor-enu`, contract version 1.0.0 | [Ethical-Tech-CoLab/digital-3d-shared-contracts](https://github.com/Ethical-Tech-CoLab/digital-3d-shared-contracts) · local: [viewer/public/frames/nyc-harbor-enu.json](viewer/public/frames/nyc-harbor-enu.json) | Programme contract | CC BY 4.0 / MIT | **read** | A | The shared ENU frame every module in this programme places into. Declares `MHW = NAVD88 + 0.59 m` within a 4000 m validity radius, which is what allows this repository to author in MHW without ever converting. Copied in byte-for-byte and hash-verified by `GRT-080`. |
| SRC-011 | **NYC DOT, *Brooklyn Bridge Promenade*, August 2016** (39 pp.) | [nyc.gov/html/dot/downloads/pdf/brooklyn-bridge-promenade.pdf](https://www.nyc.gov/html/dot/downloads/pdf/brooklyn-bridge-promenade.pdf) · local: [sources/drawings/nycdot-brooklyn-bridge-promenade.pdf](sources/drawings/nycdot-brooklyn-bridge-promenade.pdf) | **Owner's engineering study** | © City of New York; quoted and retained for citation | **read** (all 39 pages) | A | **The single most valuable modern source found.** The bridge's own owner, dimensioning the promenade end to end: a longitudinal typology with eight named sections and their lengths, a width for each, and the deck-to-girder relationship. Names the **Brooklyn Curve** and states that its extra north-side space accommodates the staircase. Also dates the 1980s Adams/Tillary ramp and the 1982 removal of the tower stairs. |
| SRC-012 | Brooklyn Bridge Park — Brooklyn Bridge access page | [brooklynbridgepark.org/places-to-see/brooklyn-bridge](https://brooklynbridgepark.org/places-to-see/brooklyn-bridge) | Official park operator | © BBP; quoted | **read** | B | "…use the Brooklyn Bridge Pedestrian Walkway which begins at the intersection of Tillary Street and Boerum Place or access the pedestrian walkway via the staircase located in the underpass on Washington Street/Cadman Plaza East and Prospect Street." Locates **both** Brooklyn-side termini by street. |
| SRC-013 | NYC Tourism + Conventions — guide to the Brooklyn Bridge | [nyctourism.com/articles/guide-to-the-brooklyn-bridge](https://www.nyctourism.com/articles/guide-to-the-brooklyn-bridge) | Official destination marketing organisation | © NYC Tourism; quoted | **read** | B | "The pedestrian stairs on the Brooklyn side are located at Washington Street and Prospect Street, right at the northeast corner of Cadman Plaza. You can also just walk straight onto the bridge from Adams Street." Independently corroborates SRC-012 on the stair location, and distinguishes the stair entrance from the Adams Street one. |
| SRC-014 | **Field observation, repository owner, 2026** | Direct observation on the bridge and in DUMBO; photographs taken outside Westville DUMBO | **Eyewitness testimony** | — | **read** | B for arrangement, D for any dimension | "Road moves to the right and walkway comes to middle going into Brooklyn. Leaving Brooklyn, cars are on right, walkway emerges from the middle. This middle area is where there are steps that tourists use to walk across the bridge to/from DUMBO. The stairs exit to Washington Street about 1.5 blocks from where I took pictures outside Westville DUMBO." **Registered because it is testimony about arrangement, and it is what prompted SRC-011 to be sought.** It may establish that an element exists and how it is arranged; it may **not** grade any dimension. |
| SRC-015 | Wikipedia — Brooklyn Bridge | [en.wikipedia.org/wiki/Brooklyn_Bridge](https://en.wikipedia.org/wiki/Brooklyn_Bridge) | Tertiary encyclopaedia | CC BY-SA | **read** | B/C | Used for exactly one control: the promenade sits 18 ft above the automobile lanes (CTL-097). Its "4 ft below the girders" statement is independently confirmed grade `A` by SRC-011, which is some evidence its 18 ft is also sound — but no primary or owner document read here states it, so it stays grade `B`. Everything else it says is already covered by a better source. |
| SRC-016 | HistoricBridges.org — Brooklyn Bridge photo galleries 3 and 4 | [gallery 3](https://historicbridges.org/bridges/browser/photosviewer.php?bridgebrowser=newyork/brooklyn/&gallerynum=3&gallerysize=2) · [gallery 4](https://historicbridges.org/bridges/browser/photosviewer.php?bridgebrowser=newyork/brooklyn/&gallerynum=4&gallerysize=2) | Modern detail photography | **© HistoricBridges.org. NOT redistributable.** | **read** — 12 full-size plates examined | B for arrangement, **never for a dimension** | The Tier B detail source the brief anticipated. **Its images are not copied into this repository and are not served from the published site**; the viewer links out to the galleries instead. What was learned from them is recorded below and in OQ-007. |
| SRC-017 | Historic-Structures.com — The Brooklyn Bridge, New York | [historic-structures.com/ny/new_york/brooklyn-bridge](https://www.historic-structures.com/ny/new_york/brooklyn-bridge/) | Secondary narrative | © Historic-Structures.com | **read** | — | Narrative construction history. **Its illustrations carry Library of Congress digital IDs** (`570574c`, `120491p` and others), which is how the HAER plates now in `sources/photos/` were identified — and then fetched from the LOC CDN at full resolution rather than copied from here. Cites no dimension this repository does not already hold from a better source. |

---

## Negative controls — sources that may NOT be used

Three similar East River suspension bridges are the most likely route to a confident wrong number in
this programme. These are registered so that cross-contamination is a **test failure**
(`STT-005`, `STT-006`) rather than a silent error.

| Source ID | What it is | Status |
|---|---|---|
| SRC-900 | **Manhattan Bridge** dimensions, as registered in `manhattan-bridge-3d/GEOMETRY-CONTROL.md` — main span 1470 ft, side spans 725 ft, total 6855 ft, deck width 120 ft, cable diameter 20.75 in, four cables, four subway tracks, stiffening truss depth 24 ft. | **MUST NEVER ENTER THIS MODEL.** This repository's `AGENT-INSTRUCTIONS.md` was adapted from that bridge's brief, so the risk is structural rather than hypothetical. |
| SRC-901 | **Williamsburg Bridge** — Haight and Patel, *Reconstruction of the Williamsburg Bridge*, AISC, 2005: stiffening truss "67 feet wide and approximately 40 feet deep". | **MUST NEVER ENTER THIS MODEL.** |
| SRC-902 | **The adapted brief's own residue.** [AGENT-INSTRUCTIONS.md](AGENT-INSTRUCTIONS.md) §6 and §13 ask for `subway_tracks: [track_1 … track_4]`. That is a Manhattan Bridge feature transferred by the adaptation. **The Brooklyn Bridge carries no rail lines.** It has none today and no read source describes any. SRC-003 records that the *original* 1883 deck was divided to give "two elevated railroad tracks, two trolley car tracks, a single-lane road, and a 15-foot-wide walkway" — all of that rail was removed in the middle of the twentieth century, and none of it was ever subway. | **NOT MODELLED, in any form.** Neither the Manhattan Bridge's subway tracks nor the Brooklyn Bridge's own removed elevated and trolley tracks appear in this model. The historic arrangement is registered as context only; putting rail on this bridge would be a claim no source supports. See OQ-012, and test `STT-008`, which forbids `subway`, `rail`, `trolley`, `elevated` and `track_n` in any part ID. |

The negative-control test does not merely check that these numbers are absent. It checks that they
are absent **as values**, in any unit, on any control row — because the failure mode is a plausible
number arriving without a label.

---

## Consulted but NOT registered

Material that was looked at and that **grades nothing**. It is listed so that the boundary between
"informed the work" and "supports a number" stays visible.

| Material | Why it is not registered |
|---|---|
| Two photographs supplied by the repository owner, from a tour site: a view along the promenade toward a tower, and a view of the bridge from DUMBO. | **No licence.** They are not committed to this repository and no control cites them. They were reviewed for orientation only. They are consistent with the model — the walkway is elevated above the roadway, the diagonal stays radiate from the tower tops as SRC-002 describes, the towers show two pointed arches. **None of that is evidence in the register's sense**, and per the rule in `HOW-TO-DESIGN.md`, a photograph cannot grade a control. |
| SRC-007, the HAER photographs | Registered but **not yet read** — the catalogue has been examined, the individual plates have not. Grade `B` when they are. |

The distinction matters most where it is most tempting to ignore. Every photograph shows the
promenade decked in timber; the material table still grades `promenade_*` as `D`, because no source
in the register says what the planks are.

### What SRC-016's photographs actually changed

Examined, not copied. Three findings, none of them a dimension:

1. **The approach supports are the wrong kind of object.** The model draws slender bents at a
   placeholder 100 ft pitch. The photographs show a **masonry arcade** carrying the Brooklyn
   approach, which is also what SRC-004 describes in words. This is recorded in OQ-007 and is a more
   serious defect than the spacing being unsourced, because the geometry is the wrong shape rather
   than the wrong size.
2. **The promenade sits above and between the roadways, and widens at the towers.** Independently
   corroborates SRC-011's typology and SRC-014's account, and confirms the model's arrangement.
3. **The stays land on the deck at regular intervals across the whole main span**, consistent with
   the fan the model derives from the sourced count. Nothing here dimensions them.

The measured drawing, not the photographs, is what moved a number: see CTL-064 and §4.2.

---

## Verification queue — registered, not yet read

Nothing below may be cited by a control until it moves into the register above.

| Item | Why it matters | Status |
|---|---|---|
| **NYCDOT record, shop and rehabilitation drawings** | The single highest-value action available. Not public: this is a **FOIL request, not a research problem**, and it has a long lead time. It would retire more open questions than everything else combined. | **To file. Week one.** |
| NYC Municipal Archives, 52 Chambers Street — original construction drawings | SRC-001 states plainly that "the original drawings are available for reference" there, and that this is *why* HAER prepared no historical report. That sentence is a direct pointer to the primary record. | Not visited |
| NYC DOT Brooklyn Bridge facts page (HTML) | The modern owner's own published figures. | **Retrieval failed** — `nyc.gov` returns HTTP 403 to a plain fetch of its HTML. Its *PDFs* serve fine, which is how SRC-011 was obtained. Worth another attempt with a browser user agent. |
| Robert M. Vogel, *Building Brooklyn Bridge: The Design and Construction, 1867–1883* (Smithsonian, 1983) | The actual origin of SRC-001's statistics table. Reading it directly would convert a transmitted table into an examined source. | Not read |
| David McCullough, *The Great Bridge* (1972) | SRC-001 calls this "what is accepted by most authorities as the standard text". Secondary, but authoritative on the historical record. | Not read |
| 2017 NYC Topobathymetric LiDAR (1 ft DEM/DSM + classified point cloud) | Aerial, so it sees the **top of the deck**: the right tool for approach grade and ground profile, useless for anything underneath. | Not retrieved |
| John A. Roebling, *Report to the New York Bridge Company on the proposed East River Bridge*, 1867 | The design report. Would carry the intended cable sag, which no read source states. | Not located online |

---

## Conflicts on record

Kept, not resolved silently. A model that hides source disagreement is lying by omission.

| Conflict | Sources | State | Resolution and reasoning |
|---|---|---|---|
| **CONF-001 — tower height above mean high water** | SRC-001: `276.6 ft`. SRC-002: `276'-6"`. SRC-003: `276.5-foot towers`. | **settled** | Value used: **276.5 ft**. SRC-002 is a measured drawing giving feet and inches; 276'-6" is 276.5 ft, and SRC-003 agrees independently. SRC-001 decimalises its other feet-and-inches values correctly (44'-6" → 44.5, 78'-6" → 78.5, 33'-9" → 33.8), so its `276.6` is a digit error, not a different measurement. SRC-001's figure is retained as CTL-021 and **not used for geometry**. |
| **CONF-002 — wires per cable** | SRC-001 and SRC-002: `5,434`. SRC-004 (1876 wire specification): "each cable composed of 6,300 parallel laid wires". | **settled** | Value used: **5,434**, the as-built count, agreed by two sources including the measured drawing. SRC-004's 6,300 is a **design-stage procurement specification** written before the cables were spun; it is recorded as CTL-047 and not used. |
| **CONF-003 — main cable diameter** | SRC-001: `15.75 in`. SRC-002: "bound diameters of 15-3/4 inches". SRC-004 (spec): "each 15 in. in diameter". SRC-003: "nearly 16 inches". | **settled** | Value used: **15.75 in**, from the as-built statement in two sources. SRC-004's 15 in is the same design-stage specification as CONF-002 and is recorded as CTL-048. |
| **CONF-004 — tower arch rise** | SRC-002: "36' ARCH HEIGHT", measured from the springing course. SRC-004: the pointed arches "have a rise of 35 feet 6 inches". | **open** | 6 in apart, and the two may not measure to the same point — SRC-004 is describing the New York tower's masonry contract, SRC-002 is a 20th-century survey of the same tower. Both recorded (CTL-030, CTL-031); the derivation uses SRC-002. See OQ-004. |
| **CONF-005 — anchorage top elevation** | SRC-004 gives the New York anchorage roadway at `89.04 ft` (front) and `85.24 ft` (rear) above high water; it also reports the **Brooklyn** anchorage masonry "brought up to 78 feet 6 inches above high water, and entirely completed … as far as it can be preparatory to cable-making". | **open** | The 78'-6" figure is a *state of works in 1875*, before the cornice and the top courses that SRC-004 elsewhere says are "to be set after the cables are made" — so it is almost certainly not the finished height. The model uses the New York anchorage's 89.04 ft and records the asymmetry as OQ-006. |
| **CONF-006 — main span figure inside SRC-004's wire specification** | SRC-004, wire specification: "one main span of 1,000 ft., and two side spans of 930 ft. each". | **settled — OCR damage** | The same document's own errata page corrects an unrelated OCR fault, and every other source gives 1,595.5 ft. The side-span figure in that sentence (930 ft) agrees with SRC-001 and SRC-002 and is used; the "1,000 ft." is treated as damaged text and is **not** recorded as a control. |
| **CONF-007 — how far the promenade actually runs** | SRC-002 dimensions the bridge from Park Row to Adams Street: 5989 ft. SRC-011's promenade typology sums to **6653 ft**. | **settled — they measure different things** | Both are right. The 664 ft difference is the promenade continuing past the bridge's Adams Street terminus: SRC-011 names that section the **Brooklyn Curve** (910 ft) and SRC-012 gives its far end as Tillary Street and Boerum Place. SRC-011 dates the ramp to Adams/Tillary to the 1980s, a century after SRC-002's structure. **The model now carries both**, and CHK-006 checks the on-structure typologies against the 1883 bridge separately. |

---

## Retrieval note — how these sources were found

The first pass used direct HTTP fetches and archival full texts. **The Tavily MCP server rejected
its key** (`Invalid API key`) on every attempt, so no web search ran during Milestone 1, and the
modern owner-published material was missed entirely — including SRC-011, which is the best modern
source for this bridge that exists in public.

The key was present in the environment the whole time; the MCP server was holding a stale copy.
Calling the Tavily REST API directly with `TAVILY_API_KEY` works, and that is how SRC-011 to SRC-013
were found. **`nyc.gov` also returns HTTP 403 to a plain fetch of its HTML pages but serves its PDFs
without complaint**, which is why the promenade study was reachable when the facts page was not.

Recorded here because the failure was silent and cost a whole milestone's worth of modern sourcing.

---

## Licences

| Material | Licence |
|---|---|
| HAER NY-18 data pages, caption pages, measured drawing, photographs | Works of the U.S. Government. No known copyright restrictions ([LOC rights statement](https://www.loc.gov/rr/print/res/114_habs.html)). |
| Roebling 1873 and 1877 reports | Public domain (pre-1929). Texts retrieved from the Internet Archive. |
| ASCE landmark page | © ASCE. Short passages quoted for scholarly citation; not redistributed. |
| This repository's own documents, control data and generated artifacts | CC BY 4.0 — see [LICENSE.md](LICENSE.md). |
| This repository's scripts and viewer | MIT — see [LICENSE.md](LICENSE.md). |
