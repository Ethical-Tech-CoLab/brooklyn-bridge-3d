# Viewer

A browser shell for the Brooklyn Bridge control skeleton. React + three.js, Vite.

```powershell
cd viewer
npm install
npm run dev        # http://localhost:5174
npm run build      # typecheck + production build into viewer/dist
```

It reads everything from `public/` at runtime and carries **no dimensions, part names or source text
of its own** — the same discipline the build pipeline follows. Swap `public/model.config.json` and
the same build serves a different source-governed model.

---

## Is this the right viewer? — the shared-contracts question

Short answer: **yes, this is the correct shape, and it is not a leftover.** But the relationship is
easy to get wrong, so it is written down here.

`digital-3d-shared-contracts` contains `packages/viewer-kernel`. That name makes it sound like a
viewer you should be using instead of this one. It is not.

| | `@d3d/viewer-kernel` | this directory |
|---|---|---|
| What it is | **Framework-agnostic decision logic.** No React, no three.js, no scene graph, no DOM beyond `fetch`. | A **shell**: renderer, camera, materials, meshes, panels. |
| What it decides | Which tiles are resident, which LOD level, geodetic ↔ scene ENU, module manifests and URN resolution, tour state, a typed event bus. | How any of that looks. |
| Who consumes it | The **host** — `dumbo-district-3d/viewer`, which is the reference shell. | Anyone opening this bridge on its own. |

`VIEWER-API.md` §7 is explicit that a module "may implement its own mode — the bridge's `inspect`,
with its part tree, dimension panel and exploded view". That is exactly what this directory is.

**The sibling bridge does the same thing.** `manhattan-bridge-3d/viewer` has no dependency on the
kernel either; it is a standalone shell, and the bridge's relationship to the programme is expressed
by *publishing a contract*, not by importing a renderer. Both viewers depend on `react`, `react-dom`
and `three`, and nothing else.

So there is no duplicate or stale viewer to remove. There is, however, a **real gap**, recorded next.

### Discrepancy: this module does not yet publish its module contract

`manhattan-bridge-3d` publishes a full contract surface that this repository does not have yet:

| Artifact | Manhattan | Brooklyn (here) | Note |
|---|---|---|---|
| `frames/nyc-harbor-enu.json` | ✅ | ✅ | **Copied byte-for-byte and hash-verified by `GRT-080`.** |

**A trap worth knowing about, because it cost a CI run.** "Copy byte-for-byte and verify by hash"
has a platform dimension that is easy to miss: **git's line-ending translation is a
re-serialisation.** With no `.gitattributes`, the frame checks out CRLF on Windows and LF on Linux,
the two hash differently, and `GRT-080` passes on a developer's machine while failing in CI. The
canonical bytes are the LF ones, because that is what git stores and what every non-Windows clone
receives.

The same defect ran deeper: Python's `write_text` uses `os.linesep`, so **the build itself emitted
CRLF on Windows**, which would have made every generated artifact differ by platform and broken the
byte-identity gate permanently. Both are fixed — `.gitattributes` pins `eol=lf`, and every text
writer in `scripts/` now passes `newline="\n"` explicitly.

| Artifact | Manhattan | Brooklyn (here) | Note |
|---|---|---|---|
| `bridge-manifest.json` (module manifest) | ✅ | ❌ | Milestone 5 |
| `bridge/asset-registry.json` | ✅ | ❌ | Milestone 5 |
| `bridge/lod.json` (LOD ladder) | ✅ | ❌ | Milestone 5 |
| `assets/bridge.lod2.glb` (level-2 proxy) | ✅ | ❌ | Milestone 5 |
| `scripts/publish_module_contract.py` | ✅ | ❌ | Milestone 5 |
| `scripts/validate_contract.mjs` | ✅ | ❌ | Milestone 5 |

`HOW-TO-DESIGN.md` §12 argues for publishing the contract *early*, because it surfaces
coordinate-frame disagreements while they are still theoretical. That advice is accepted, and the
cheapest half of it is done now: the canonical frame is present, byte-identical to the copies held by
`digital-3d-shared-contracts`, `manhattan-bridge-3d` and `dumbo-district-3d`, and a test fails if it
is ever re-serialised.

The rest is deliberately deferred, for one honest reason: **this module has no placement to
publish.** OQ-008 records that the real-world azimuth and origin of the bridge axis are not in the
register, and SRC-008's LOC coordinate locates the *catalogue record*, not a structural element, so
it cannot verify one. Publishing a manifest with a georeference we cannot defend would be precisely
the failure this repository exists to prevent. The manifest lands when the placement is sourced.

One thing the frame gave us immediately: it declares `MHW = NAVD88 + 0.59 m` within a 4000 m
validity radius. That answers OQ-009. The offset is **recorded and not applied** — the model stays
in mean high water because that is the datum its sources use, and the conversion belongs at
placement time.

---

## What the viewer does

Everything below is a requirement from `CONFIDENCE-MODEL.md` §3 or `AGENT-INSTRUCTIONS.md` §10.

- **Provenance is drawn into the geometry**, not only into a side panel: `DOCUMENTED` renders solid
  and opaque, `INFERRED` at reduced opacity with a **dashed** outline, `ASSUMED` faint with a
  **dotted** outline.
- **The filter hides, it does not fade.** Switching `INFERRED` and `ASSUMED` off leaves the towers,
  the anchorages, the deck chain and the station markers. That near-empty frame is the honest
  picture of what the sources actually locate, and it is published rather than hidden.
- **Locus on selection.** Selecting a part lists the control rows its geometry rests on, with their
  grades, values and source IDs — or says plainly that there are none.
- **A standing tally**, sticky at the top of the right rail, never below the fold.
- **No dimension is shown for an `ASSUMED` part.** The extent block is replaced by a statement of
  why.
- **HO toggle** swaps to `control_skeleton_ho.glb` and reports every extent in millimetres. The
  provenance and confidence metadata are unchanged — dividing a placeholder by 87.1 does not make it
  a measurement.
- **Materials come from the control document**, not the renderer, and the material table has no
  default rule.

### three.js notes

- `LineDashedMaterial` renders **solid** unless `computeLineDistances()` is called after the
  geometry is built. Both dashed and dotted outlines call it.
- The canvas is given an **explicit initial size** rather than relying on `ResizeObserver` alone. A
  headless page may never fire it, and a canvas sized only from it reports zero width, which makes
  screenshots fail.
- Dev servers should be **detached** if you want them to outlive the shell that started them.

---

## Files

```text
index.html            entry
src/main.tsx          React root
src/App.tsx           data loading, filter state, layout
src/BridgeViewer.tsx  three.js scene, provenance rendering, picking
src/model.ts          runtime types, provenance/confidence rules, document-relative fetch
src/styles.css
components/           Toolbar, PartTree, ProvenancePanel, MetadataPanel, ConfidenceLegend
public/               the published surface — GLBs, parts.json, controls.json,
                      build_report.json, model.config.json, frames/nyc-harbor-enu.json
```

`public/` is regenerated by `python scripts/build_control_skeleton.py`. Do not hand-edit it.
