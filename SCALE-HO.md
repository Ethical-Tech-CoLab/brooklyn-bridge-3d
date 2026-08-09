# HO Scale Reference

**Reporting scale: 1 : 87.1.** The model is authored at full prototype size in meters. HO is a
*reporting and export* transform, never an authoring one.

---

## 1. Why the model is not authored in HO

Authoring at scale bakes a rounding decision into the geometry, and it is irreversible. Authoring at
prototype size keeps every number identical to the source that supplied it, so a control row can be
compared with its source by eye, in the unit the source used.

The single conversion implementation lives in [scripts/normalize_units.py](scripts/normalize_units.py).
Nothing else in the repository converts units.

---

## 2. The transform

```text
ho_meters      = prototype_meters / 87.1
ho_millimeters = ho_meters * 1000
ho_inches      = ho_meters / 0.0254
```

`scripts/build_control_skeleton.py` emits a second GLB, `control_skeleton_ho.glb`, that is the
prototype model divided by 87.1, and a per-control table at `viewer/metadata/scale_ho.json`.

---

## 3. Worked figures

Derived from the control document, not typed in. Run `python scripts/normalize_units.py` to
regenerate the full table.

| Control | Key | Prototype | HO (mm) | HO (in) |
|---|---|---:|---:|---:|
| CTL-001 | main_span | 1595.5 ft (486.31 m) | 5583.4 | 219.82 |
| CTL-004 | total_length_including_approaches | 5989 ft (1825.45 m) | 20957.0 | 825.08 |
| CTL-020 | tower_height_above_mhw | 276.5 ft (84.28 m) | 967.6 | 38.09 |
| CTL-070 | deck_width | 85 ft (25.91 m) | 297.5 | 11.71 |
| CTL-041 | main_cable_diameter | 15.75 in (0.40 m) | 4.6 | 0.180 |

**The model is 21 metres long in HO.** A complete HO Brooklyn Bridge is not a table-top object; it is
a room. Treat the full bridge as a digital twin first and extract modular study pieces later — a
single tower is 968 mm tall, which *is* a buildable object.

---

## 4. Rounding

Rounding happens **at report time only**, never in the authoring data:

- `ho_mm` — 2 decimal places below 10 mm, 1 above.
- `ho_in` — 3 decimal places below 1 in, 2 above.
- Prototype values are carried at full precision through the pipeline.

A part whose HO dimension rounds to `0.0` mm is reported by `GRT-021` — below roughly 0.05 mm nothing
survives any physical process, so such a part is a rendering detail rather than a scale component.

---

## 5. What HO does not do

HO output carries the **same** provenance and confidence metadata as the prototype model. Dividing a
placeholder by 87.1 does not make it a measurement. A part whose provenance is `ASSUMED` is excluded
from HO dimension callouts exactly as it is from prototype ones.
