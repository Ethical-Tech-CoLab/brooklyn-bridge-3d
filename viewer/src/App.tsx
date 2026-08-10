import { useEffect, useMemo, useState } from 'react';
import BridgeViewer from './BridgeViewer';
import ComparePanel from '../components/ComparePanel';
import CompareStage from '../components/CompareStage';
import ConfidenceLegend from '../components/ConfidenceLegend';
import MetadataPanel, { type ControlRow } from '../components/MetadataPanel';
import PartTree from '../components/PartTree';
import ProvenancePanel from '../components/ProvenancePanel';
import Toolbar from '../components/Toolbar';
import {
  loadJson,
  NUDGE_IDENTITY,
  type BuildReport,
  type CompareMode,
  type ModelConfig,
  type Nudge,
  type Part,
  type PartsDocument,
  type Provenance,
  type ReferenceView,
  type ReferenceViewsDocument,
} from './model';

interface ControlsDocument {
  control_document_sha256: string;
  controls: ControlRow[];
}

export default function App() {
  const [config, setConfig] = useState<ModelConfig | null>(null);
  const [partsDoc, setPartsDoc] = useState<PartsDocument | null>(null);
  const [report, setReport] = useState<BuildReport | null>(null);
  const [controlsDoc, setControlsDoc] = useState<ControlsDocument | null>(null);
  const [error, setError] = useState<string | null>(null);

  const [hiddenSystems, setHiddenSystems] = useState<Set<string>>(new Set());
  const [hiddenProvenance, setHiddenProvenance] = useState<Set<Provenance>>(new Set());
  const [selected, setSelected] = useState<string | null>(null);
  const [hoScale, setHoScale] = useState(false);
  const [triangles, setTriangles] = useState(0);

  const [refs, setRefs] = useState<ReferenceViewsDocument | null>(null);
  const [activeRef, setActiveRef] = useState<ReferenceView | null>(null);
  const [compareMode, setCompareMode] = useState<CompareMode>('off');
  const [nudge, setNudge] = useState<Nudge>(NUDGE_IDENTITY);
  const [poseNonce, setPoseNonce] = useState(0);

  useEffect(() => {
    (async () => {
      try {
        const cfg = await loadJson<ModelConfig>('model.config.json');
        const [parts, buildReport, controls] = await Promise.all([
          loadJson<PartsDocument>(cfg.parts),
          loadJson<BuildReport>(cfg.build_report),
          loadJson<ControlsDocument>('controls.json'),
        ]);
        if (parts.control_document_sha256 !== buildReport.control_document_sha256) {
          throw new Error(
            'parts.json and build_report.json were built from different control documents',
          );
        }
        setConfig(cfg);
        setPartsDoc(parts);
        setReport(buildReport);
        setControlsDoc(controls);
        // Reference imagery is optional: a module that ships none simply has no compare panel.
        try {
          setRefs(await loadJson<ReferenceViewsDocument>('reference-views.json'));
        } catch {
          setRefs(null);
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : String(err));
      }
    })();
  }, []);

  const partMap = useMemo(() => {
    const map = new Map<string, Part>();
    for (const part of partsDoc?.parts ?? []) map.set(part.part_id, part);
    return map;
  }, [partsDoc]);

  const controlMap = useMemo(() => {
    const map = new Map<string, ControlRow>();
    for (const row of controlsDoc?.controls ?? []) map.set(row.control_id, row);
    return map;
  }, [controlsDoc]);

  if (error) {
    return (
      <div className="fatal">
        <h1>Could not load the model</h1>
        <p>{error}</p>
        <p className="hint">Run <code>python scripts/build_control_skeleton.py</code> and reload.</p>
      </div>
    );
  }
  if (!config || !partsDoc || !report || !controlsDoc) {
    return <div className="fatal"><p>Loading…</p></div>;
  }

  const toggle = <T,>(set: Set<T>, value: T): Set<T> => {
    const next = new Set(set);
    if (next.has(value)) next.delete(value);
    else next.add(value);
    return next;
  };

  const viewport = (
    <BridgeViewer
      assetUrl={hoScale ? config.assets.ho : config.assets.prototype}
      parts={partMap}
      hiddenSystems={hiddenSystems}
      hiddenProvenance={hiddenProvenance}
      selected={selected}
      onSelect={setSelected}
      onLoaded={({ triangles: t }) => setTriangles(t)}
      pose={activeRef?.camera ?? null}
      poseNonce={poseNonce}
    />
  );

  const pickRef = (view: ReferenceView | null) => {
    setActiveRef(view);
    setNudge(NUDGE_IDENTITY);
    if (view) {
      setPoseNonce((n) => n + 1);
      if (compareMode === 'off') setCompareMode('overlay');
    } else {
      setCompareMode('off');
    }
  };

  return (
    <div className="app">
      <Toolbar
        config={config}
        report={report}
        hoScale={hoScale}
        onToggleHo={() => setHoScale((v) => !v)}
        triangles={triangles}
      />
      <main>
        <aside className="rail left">
          <PartTree
            parts={partsDoc.parts}
            hiddenSystems={hiddenSystems}
            hiddenProvenance={hiddenProvenance}
            selected={selected}
            onToggleSystem={(system) => setHiddenSystems((s) => toggle(s, system))}
            onSelect={setSelected}
          />
          {refs && (
            <ComparePanel
              doc={refs}
              activeId={activeRef?.id ?? null}
              mode={compareMode}
              nudge={nudge}
              onPick={pickRef}
              onMode={setCompareMode}
              onNudge={(patch) => setNudge((n) => ({ ...n, ...patch }))}
              onRecall={() => setPoseNonce((n) => n + 1)}
              onReset={() => setNudge(NUDGE_IDENTITY)}
            />
          )}
        </aside>

        {activeRef && compareMode !== 'off' ? (
          <CompareStage view={activeRef} mode={compareMode} nudge={nudge}>
            {viewport}
          </CompareStage>
        ) : (
          viewport
        )}

        <aside className="rail right">
          <ProvenancePanel
            report={report}
            hidden={hiddenProvenance}
            onToggle={(state) => setHiddenProvenance((s) => toggle(s, state))}
          />
          <MetadataPanel
            part={selected ? (partMap.get(selected) ?? null) : null}
            controls={controlMap}
            hoScale={hoScale}
            hoDenominator={partsDoc.ho_scale_denominator}
          />
          <ConfidenceLegend report={report} />
          <section className="panel">
            <h2>Build</h2>
            <p className="hint">
              Control document <code>{report.control_document_sha256.slice(0, 12)}</code> ·{' '}
              {report.controls_sourced} sourced controls · {report.controls_placeholder} placeholders
            </p>
            <ul className="checks">
              {report.derived.checks.map((check) => (
                <li key={check.id} className={check.passed ? 'good' : 'bad'}>
                  <code>{check.id}</code> {check.residual_ft >= 0 ? '+' : ''}
                  {check.residual_ft.toFixed(3)} ft — {check.description}
                </li>
              ))}
            </ul>
            <p className="hint">
              <a href={config.repository} target="_blank" rel="noreferrer">
                Sources, conflicts and open questions
              </a>
            </p>
          </section>
        </aside>
      </main>
    </div>
  );
}
