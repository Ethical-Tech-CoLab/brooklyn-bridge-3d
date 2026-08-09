import type { BuildReport, ModelConfig } from '../src/model';

interface Props {
  config: ModelConfig;
  report: BuildReport;
  hoScale: boolean;
  onToggleHo: () => void;
  triangles: number;
}

export default function Toolbar({ config, report, hoScale, onToggleHo, triangles }: Props) {
  const failing = report.derived.checks.filter((c) => !c.passed).length;
  return (
    <header className="toolbar">
      <div className="brand">
        <h1>{config.name}</h1>
        <span>{config.subtitle}</span>
      </div>
      <div className="toolbar-facts">
        <span title="Every elevation in this model is relative to mean high water and is never converted.">
          datum <b>{config.vertical_datum}</b>
        </span>
        <span>
          sag <b>{report.derived.cable_sag_ft} ft</b> (1:{report.derived.cable_sag_ratio}){' '}
          <span className={`grade grade-${report.derived.cable_sag_confidence}`}>
            {report.derived.cable_sag_confidence}
          </span>
        </span>
        <span>
          suspender pitch <b>{report.derived.suspender_pitch_ft} ft</b>
        </span>
        <span>{triangles.toLocaleString()} triangles</span>
        <span className={failing ? 'bad' : 'good'}>
          {report.derived.checks.length - failing}/{report.derived.checks.length} build checks pass
        </span>
      </div>
      <button type="button" className={`ho ${hoScale ? 'on' : ''}`} onClick={onToggleHo}>
        {hoScale ? 'HO 1:87.1' : 'Prototype'}
      </button>
    </header>
  );
}
