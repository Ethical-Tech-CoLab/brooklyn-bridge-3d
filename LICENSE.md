# License

This repository contains two kinds of material, licensed separately.

## Research content and data — CC BY 4.0

The governance documents, control data, source register, test definitions and generated model
artifacts are licensed under the
[Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).

This covers:

```text
README.md, AGENT-INSTRUCTIONS.md, GEOMETRY-CONTROL.md, SOURCE-REGISTER.md,
CONFIDENCE-MODEL.md, SCALE-HO.md
tests/*.json
viewer/metadata/*.json
cad/procedural/control_skeleton_geometry.json
mesh/glb/*
```

You are free to share and adapt this material for any purpose, including commercially, provided you
give appropriate credit and indicate if changes were made.

Cite as:

> *Brooklyn Bridge Digital Twin: a source-governed control skeleton.* Ethical Tech CoLab, 2026.

## Code — MIT

The build pipeline and the browser viewer are licensed under the MIT License.

This covers:

```text
scripts/*.py
cad/procedural/build_in_blender.py
viewer/src/*, viewer/components/*, viewer/*.ts, viewer/*.json, viewer/index.html
```

```text
MIT License

Copyright (c) 2026 Ethical Tech CoLab

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Incorporated material

**Ethical Tech CoLab, `manhattan-bridge-3d`, CC BY 4.0 / MIT.** `HOW-TO-DESIGN.md`, the confidence
and provenance model, and the three bridge-agnostic scripts `scripts/control_model.py`,
`scripts/normalize_units.py` and `scripts/export_gltf.py` are carried over from that repository
under its licence. The Manhattan Bridge's *dimensions* are deliberately **not** carried over; they
are registered in [SOURCE-REGISTER.md](SOURCE-REGISTER.md) as a negative control.

**Federal records.** HAER No. NY-18 — the data pages, the caption pages and the single measured
drawing — are works of the U.S. Government with no known copyright restrictions. Retrieved copies
are held in [sources/drawings/](sources/drawings) and are redistributed here on that basis.

**Period engineering sources.** Washington A. Roebling, *Report of the Chief Engineer of the New
York & Brooklyn Bridge* (1877) and *Pneumatic Tower Foundations of the East River Suspension Bridge*
(1873) are in the public domain. Full texts are held in [sources/drawings/](sources/drawings).

**Quoted material.** Short passages are quoted from other engineering literature for scholarly
commentary and citation. Those passages remain the property of their respective authors and
publishers. Individual sources, their licences and their verification state are recorded in
[SOURCE-REGISTER.md](SOURCE-REGISTER.md).
