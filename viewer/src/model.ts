export interface ReferenceCamera {
  projection: 'perspective' | 'orthographic';
  position: [number, number, number];
  target: [number, number, number];
  up: [number, number, number];
  fov_y_deg?: number;
  ortho_height_m?: number;
}

export interface ReferenceView {
  id: string;
  title: string;
  subtitle?: string;
  kind: 'drawing' | 'photograph';
  image: string;
  source_id: string;
  credit: string;
  license: string;
  source_url?: string;
  camera: ReferenceCamera;
  pose_confidence: Confidence;
  notes?: string;
}

export interface ReferenceLink {
  id: string;
  title: string;
  publisher: string;
  url: string;
  license: string;
  source_id: string;
  notes?: string;
}

export interface ReferenceViewsDocument {
  contract_version: string;
  kind: 'reference-views';
  module: string;
  description?: string;
  pose_disclaimer: string;
  views: ReferenceView[];
  /**
   * Reference material that may NOT be redistributed. Linked out rather than embedded, so a
   * copyrighted gallery can still be part of the review path without being copied.
   */
  links?: ReferenceLink[];
}

export type CompareMode = 'off' | 'overlay' | 'split';

/** Manual fine-alignment applied on top of a declared pose. Never persisted into the contract. */
export interface Nudge {
  scale: number;
  dx: number;
  dy: number;
  opacity: number;
}

export const NUDGE_IDENTITY: Nudge = { scale: 1, dx: 0, dy: 0, opacity: 0.5 };

/**
 * Runtime model description. Everything the viewer knows about the bridge is loaded from
 * `public/` at runtime — the viewer carries no dimensions, no part names and no source text of its
 * own, exactly as the build pipeline carries no numbers of its own.
 */

export type Provenance = 'MEASURED' | 'DOCUMENTED' | 'INFERRED' | 'ASSUMED';
export type Confidence = 'A' | 'B' | 'C' | 'D';

export interface Part {
  part_id: string;
  system: string;
  subsystem: string;
  source_basis: string[];
  control_refs: string[];
  confidence: Confidence;
  provenance: Provenance;
  material: string;
  material_id: string;
  material_confidence: Confidence;
  open_questions: string[];
  prototype_units: string;
  ho_scale_units: string;
  bbox_min_m: [number, number, number];
  bbox_max_m: [number, number, number];
  notes: string;
  review_status: string;
  last_modified_by_agent: string;
}

export interface PartsDocument {
  control_document_sha256: string;
  generator: string;
  vertical_datum: string;
  units: string;
  ho_scale_denominator: number;
  parts: Part[];
}

export interface BuildCheck {
  id: string;
  description: string;
  residual_ft: number;
  tolerance_m: number;
  passed: boolean;
}

export interface BuildReport {
  control_document_sha256: string;
  controls_total: number;
  controls_sourced: number;
  controls_placeholder: number;
  parts_total: number;
  provenance: Record<Provenance, number>;
  confidence: Record<Confidence, number>;
  systems: string[];
  derived: {
    stations_m: Record<string, number>;
    elevations_m: Record<string, number>;
    cable_sag_ft: number;
    cable_sag_ratio: number;
    cable_sag_confidence: Confidence;
    suspender_pitch_ft: number;
    suspenders_per_cable: number;
    deck_chain_ids: string[];
    checks: BuildCheck[];
  };
}

export interface ModelConfig {
  name: string;
  subtitle: string;
  assets: { prototype: string; ho: string };
  parts: string;
  build_report: string;
  vertical_datum: string;
  repository: string;
}

/** Provenance rendering rules — CONFIDENCE-MODEL.md section 3. */
export const PROVENANCE_ORDER: Provenance[] = ['MEASURED', 'DOCUMENTED', 'INFERRED', 'ASSUMED'];

export const PROVENANCE_STYLE: Record<
  Provenance,
  { opacity: number; outline: 'solid' | 'dashed' | 'dotted'; dash: number; gap: number; label: string }
> = {
  MEASURED: { opacity: 1.0, outline: 'solid', dash: 0, gap: 0, label: 'instrument reading' },
  DOCUMENTED: { opacity: 1.0, outline: 'solid', dash: 0, gap: 0, label: 'stated in a source that was read' },
  INFERRED: { opacity: 0.55, outline: 'dashed', dash: 2.5, gap: 1.5, label: 'exists in a source; shape reasoned' },
  ASSUMED: { opacity: 0.28, outline: 'dotted', dash: 0.4, gap: 1.6, label: 'nothing sourced locates it' },
};

export const CONFIDENCE_LABEL: Record<Confidence, string> = {
  A: 'official record, measured drawing, or period primary',
  B: 'consistent across read sources, or one source plus control geometry',
  C: 'from an aligned mesh, photogrammetry or coordinate',
  D: 'placeholder — no source states it',
};

/**
 * Document-relative fetch. Using a relative URL means one build works both standalone and when the
 * viewer is co-served under a district site root; both layouts are asserted in the README.
 */
export async function loadJson<T>(path: string): Promise<T> {
  const response = await fetch(new URL(path, document.baseURI));
  if (!response.ok) throw new Error(`${path}: HTTP ${response.status}`);
  return (await response.json()) as T;
}
