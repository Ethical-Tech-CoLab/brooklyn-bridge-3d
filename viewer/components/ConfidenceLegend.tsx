import { CONFIDENCE_LABEL, type BuildReport, type Confidence } from '../src/model';

const GRADES: Confidence[] = ['A', 'B', 'C', 'D'];

export default function ConfidenceLegend({ report }: { report: BuildReport }) {
  return (
    <section className="panel">
      <h2>Source confidence</h2>
      <p className="hint">
        A separate axis from provenance. A source can be fully read and still support only a
        reasoned position.
      </p>
      <ul className="legend">
        {GRADES.map((grade) => (
          <li key={grade}>
            <span className={`grade grade-${grade}`}>{grade}</span>
            <span className="legend-count">{report.confidence[grade] ?? 0} parts</span>
            <span className="legend-meaning">{CONFIDENCE_LABEL[grade]}</span>
          </li>
        ))}
      </ul>
    </section>
  );
}
