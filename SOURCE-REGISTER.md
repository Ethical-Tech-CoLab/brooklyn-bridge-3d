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

## Verification queue — registered, not yet read

Nothing below may be cited by a control until it moves into the register above.

| Item | Why it matters | Status |
|---|---|---|
| **NYCDOT record, shop and rehabilitation drawings** | The single highest-value action available. Not public: this is a **FOIL request, not a research problem**, and it has a long lead time. It would retire more open questions than everything else combined. | **To file. Week one.** |
| NYC Municipal Archives, 52 Chambers Street — original construction drawings | SRC-001 states plainly that "the original drawings are available for reference" there, and that this is *why* HAER prepared no historical report. That sentence is a direct pointer to the primary record. | Not visited |
| NYC DOT Brooklyn Bridge facts page | The modern owner's own published figures. | **Retrieval failed** — `nyc.gov` returned HTTP 403 to every attempt on 2026-08-09. Not read, therefore not cited anywhere. |
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

---

## Licences

| Material | Licence |
|---|---|
| HAER NY-18 data pages, caption pages, measured drawing, photographs | Works of the U.S. Government. No known copyright restrictions ([LOC rights statement](https://www.loc.gov/rr/print/res/114_habs.html)). |
| Roebling 1873 and 1877 reports | Public domain (pre-1929). Texts retrieved from the Internet Archive. |
| ASCE landmark page | © ASCE. Short passages quoted for scholarly citation; not redistributed. |
| This repository's own documents, control data and generated artifacts | CC BY 4.0 — see [LICENSE.md](LICENSE.md). |
| This repository's scripts and viewer | MIT — see [LICENSE.md](LICENSE.md). |
