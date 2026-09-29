import React, { useMemo } from 'react';
import './PlumbGraph.css';
import { RunState } from '../lib/types';
import { computeGraphLayout } from './geometry';

interface PlumbGraphProps {
  state: RunState;
  width?: number;
  height?: number;
  onCandidateSelect?: (id: string) => void;
}

export default function PlumbGraph({ state, width = 600, height = 400, onCandidateSelect }: PlumbGraphProps) {
  const layout = useMemo(() => computeGraphLayout(state, width, height), [state, width, height]);

  return (
    <div className="plumb-graph-container">
      <svg width={width} height={height} role="img" aria-label="Plumb graph visualizing candidate runs">
        {/* Baseline */}
        <line x1={layout.baselineX} y1={layout.anchor.y} x2={layout.baselineX} y2={height} className="plumb-baseline" />
        
        {/* Anchor */}
        <circle cx={layout.anchor.x} cy={layout.anchor.y} r={6} className="plumb-anchor" />

        {/* Checkpoints */}
        {layout.checkpoints.map((cp, i) => (
          <circle key={i} cx={cp.x} cy={cp.y} r={4} className="plumb-checkpoint" />
        ))}

        {/* Candidates */}
        {layout.candidates.map((c) => {
          const start = c.points[0];
          const end = c.points[1];
          if (!start || !end) return null;
          return (
            <g key={c.id} className="plumb-candidate" onClick={() => onCandidateSelect?.(c.id)}>
              <line x1={start.x} y1={start.y} x2={end.x} y2={end.y} className="plumb-cable" />
              <circle cx={end.x} cy={end.y} r={8} className="plumb-bob" />
            </g>
          );
        })}
      </svg>
    </div>
  );
}
