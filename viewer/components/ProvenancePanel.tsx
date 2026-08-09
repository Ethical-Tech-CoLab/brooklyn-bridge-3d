import { PROVENANCE_ORDER, PROVENANCE_STYLE, type BuildReport, type Provenance } from '../src/model';

interface Props {
  report: BuildReport;
  hidden: Set<Provenance>;
  onToggle: (state: Provenance) => void;
}

/**
 * The standing tally. Permanently on screen, not below the fold of a scrolling list — a buried
 * count is the thing VISUAL-MODEL-FRAMEWORK warns against.
 */
export default function ProvenancePanel({ report, hidden, onToggle }: Props) {
  const total = report.parts_total;
  return (
    <section className="panel tally">
      <h2>Provenance</h2>
      <p className="hint">How the shape and position of each part is known. The filter hides; it does not fade.</p>
      <ul className="tally-list">
        {PROVENANCE_ORDER.map((state) => {
          const count = report.provenance[state] ?? 0;
          const style = PROVENANCE_STYLE[state];
          const off = hidden.has(state);
          return (
            <li key={state} className={off ? 'off' : ''}>
              <label>
                <input type="checkbox" checked={!off} onChange={() => onToggle(state)} />
                <span className={`swatch outline-${style.outline}`} aria-hidden />
                <span className="tally-name">{state}</span>
                <span className="tally-count">{count}</span>
              </label>
              <span className="tally-meaning">{style.label}</span>
            </li>
          );
        })}
      </ul>
      <p className="tally-total">
        {total} parts · {report.controls_sourced} sourced controls · {report.controls_placeholder} placeholders
      </p>
      {report.provenance.MEASURED === 0 && (
        <p className="hint warn">
          Nothing in this model is <strong>MEASURED</strong>. No survey or photogrammetry has been
          ingested. This count is computed, not hardcoded, so it will change on its own the day one is.
        </p>
      )}
      {hidden.has('INFERRED') && hidden.has('ASSUMED') && (
        <p className="hint warn">
          With inferred and assumed geometry switched off, what remains is what the sources actually
          locate. That emptiness is the honest picture, and it is published rather than hidden.
        </p>
      )}
    </section>
  );
}
