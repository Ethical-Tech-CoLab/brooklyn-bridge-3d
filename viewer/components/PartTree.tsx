import { useMemo, useState } from 'react';
import type { Part, Provenance } from '../src/model';

interface Props {
  parts: Part[];
  hiddenSystems: Set<string>;
  hiddenProvenance: Set<Provenance>;
  selected: string | null;
  onToggleSystem: (system: string) => void;
  onSelect: (partId: string) => void;
}

export default function PartTree(props: Props) {
  const [open, setOpen] = useState<Set<string>>(new Set(['towers', 'anchorages']));

  const bySystem = useMemo(() => {
    const map = new Map<string, Part[]>();
    for (const part of props.parts) {
      const list = map.get(part.system) ?? [];
      list.push(part);
      map.set(part.system, list);
    }
    return [...map.entries()].sort((a, b) => a[0].localeCompare(b[0]));
  }, [props.parts]);

  return (
    <section className="panel tree">
      <h2>Components</h2>
      <p className="hint">Toggle a system, or select a part to see what its geometry rests on.</p>
      {bySystem.map(([system, parts]) => {
        const hidden = props.hiddenSystems.has(system);
        const expanded = open.has(system);
        const visibleCount = parts.filter((p) => !props.hiddenProvenance.has(p.provenance)).length;
        return (
          <div key={system} className={`tree-system ${hidden ? 'off' : ''}`}>
            <div className="tree-system-head">
              <input
                type="checkbox"
                checked={!hidden}
                onChange={() => props.onToggleSystem(system)}
                aria-label={`show ${system}`}
              />
              <button
                type="button"
                className="tree-toggle"
                onClick={() =>
                  setOpen((prev) => {
                    const next = new Set(prev);
                    if (next.has(system)) next.delete(system);
                    else next.add(system);
                    return next;
                  })
                }
              >
                {expanded ? '▾' : '▸'} {system.replace(/_/g, ' ')}
                <span className="tree-count">
                  {visibleCount}/{parts.length}
                </span>
              </button>
            </div>
            {expanded && (
              <ul>
                {parts.map((part) => (
                  <li key={part.part_id}>
                    <button
                      type="button"
                      className={`tree-part prov-${part.provenance.toLowerCase()} ${
                        props.selected === part.part_id ? 'selected' : ''
                      }`}
                      onClick={() => props.onSelect(part.part_id)}
                    >
                      <span className={`grade grade-${part.confidence}`}>{part.confidence}</span>
                      {part.part_id}
                    </button>
                  </li>
                ))}
              </ul>
            )}
          </div>
        );
      })}
    </section>
  );
}
