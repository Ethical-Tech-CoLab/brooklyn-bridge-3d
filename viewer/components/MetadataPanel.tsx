import type { Part } from '../src/model';
import { PROVENANCE_STYLE } from '../src/model';

export interface ControlRow {
  control_id: string;
  key: string;
  value: number;
  unit: string;
  source_ids: string[];
  confidence: string;
  is_placeholder: boolean;
  notes: string;
}

interface Props {
  part: Part | null;
  controls: Map<string, ControlRow>;
  hoScale: boolean;
  hoDenominator: number;
}

function size(part: Part, axis: 0 | 1 | 2) {
  return part.bbox_max_m[axis] - part.bbox_min_m[axis];
}

/**
 * Locus on selection. Selecting a part shows the control rows its geometry actually rests on — or
 * says plainly that there are none. A dimension is never shown for an ASSUMED part.
 */
export default function MetadataPanel({ part, controls, hoScale, hoDenominator }: Props) {
  if (!part) {
    return (
      <section className="panel">
        <h2>Selection</h2>
        <p className="hint">Click a part in the model, or pick one from the component tree.</p>
      </section>
    );
  }

  const rows = part.control_refs.map((id) => controls.get(id)).filter(Boolean) as ControlRow[];
  const sourced = rows.filter((r) => !r.is_placeholder);
  const placeholders = rows.filter((r) => r.is_placeholder);
  const style = PROVENANCE_STYLE[part.provenance];
  const dimensionsAllowed = part.provenance !== 'ASSUMED';
  const factor = hoScale ? 1000 / hoDenominator : 1;
  const unit = hoScale ? 'mm' : 'm';

  return (
    <section className="panel">
      <h2>{part.part_id}</h2>
      <dl className="meta">
        <dt>System</dt>
        <dd>
          {part.system} / {part.subsystem}
        </dd>
        <dt>Provenance</dt>
        <dd>
          <span className={`prov-tag prov-${part.provenance.toLowerCase()}`}>{part.provenance}</span>{' '}
          <span className="hint inline">{style.label}</span>
        </dd>
        <dt>Confidence</dt>
        <dd>
          <span className={`grade grade-${part.confidence}`}>{part.confidence}</span>{' '}
          <span className="hint inline">weakest link across {rows.length} control rows</span>
        </dd>
        <dt>Material</dt>
        <dd>
          {part.material}{' '}
          <span className="hint inline">
            {part.material_id}, graded {part.material_confidence} on its own axis
          </span>
        </dd>
      </dl>

      <h3>Extent</h3>
      {dimensionsAllowed ? (
        <ul className="dims">
          <li>
            along bridge <b>{(size(part, 0) * factor).toFixed(hoScale ? 1 : 2)} {unit}</b>
          </li>
          <li>
            across bridge <b>{(size(part, 1) * factor).toFixed(hoScale ? 1 : 2)} {unit}</b>
          </li>
          <li>
            vertical <b>{(size(part, 2) * factor).toFixed(hoScale ? 1 : 2)} {unit}</b>
          </li>
        </ul>
      ) : (
        <p className="hint warn">
          No dimension is shown. This part's provenance is <strong>ASSUMED</strong> — nothing in the
          register locates it, so we do not get to say how big it is.
        </p>
      )}

      <h3>What this rests on</h3>
      {sourced.length > 0 ? (
        <ul className="controls">
          {sourced.map((row) => (
            <li key={row.control_id}>
              <span className={`grade grade-${row.confidence}`}>{row.confidence}</span>
              <code>{row.control_id}</code> {row.key} = <b>{row.value} {row.unit}</b>
              <span className="src">{row.source_ids.join(', ')}</span>
              {row.notes && <p className="note">{row.notes}</p>}
            </li>
          ))}
        </ul>
      ) : (
        <p className="hint warn">No sourced control supports this part's position.</p>
      )}

      {placeholders.length > 0 && (
        <>
          <h3>Placeholders it depends on</h3>
          <ul className="controls placeholders">
            {placeholders.map((row) => (
              <li key={row.control_id}>
                <span className="grade grade-D">D</span>
                <code>{row.control_id}</code> {row.key} = <b>{row.value} {row.unit}</b>
                <span className="src">no source</span>
                {row.notes && <p className="note">{row.notes}</p>}
              </li>
            ))}
          </ul>
        </>
      )}

      {part.open_questions.length > 0 && (
        <p className="oq">
          Open questions: {part.open_questions.join(', ')}
        </p>
      )}
      {part.notes && <p className="note part-note">{part.notes}</p>}
    </section>
  );
}
