import { useState, useMemo } from 'react';
import './PlumbGraph.css';
import { RunState } from '../lib/types';
import { computeGraphLayout } from './geometry';
import PlumbGraphTable from './PlumbGraphTable';

interface PlumbGraphProps {
  state: RunState;
  width?: number;
  height?: number;
  onCandidateSelect?: (id: string) => void;
}

export default function PlumbGraph({
  state,
  width = 620,
  height = 460,
  onCandidateSelect,
}: PlumbGraphProps) {
  const [showTable, setShowTable] = useState(false);
  const [hoveredCandidate, setHoveredCandidate] = useState<string | null>(null);

  const layout = useMemo(() => computeGraphLayout(state, width, height), [state, width, height]);

  const activeCandidateData = useMemo(() => {
    if (!hoveredCandidate) return null;
    const cand = state.candidates.find(c => c.id === hoveredCandidate);
    const layoutCand = layout.candidates.find(c => c.id === hoveredCandidate);
    if (!cand || !layoutCand) return null;
    return {
      ...cand,
      ...layoutCand,
    };
  }, [hoveredCandidate, state.candidates, layout.candidates]);

  if (showTable) {
    return (
      <div className="plumb-graph-wrapper">
        <div className="graph-toolbar">
          <button className="view-toggle-btn" onClick={() => setShowTable(false)}>
            Show as Graph
          </button>
        </div>
        <PlumbGraphTable state={state} />
      </div>
    );
  }

  const ariaSummary = `Plumb graph. Current stage ${state.currentStage} of 6. ${state.candidates.length} candidates. Verdict: ${state.verdict || 'in progress'}.`;

  return (
    <div className="plumb-graph-wrapper">
      <div className="graph-toolbar">
        <span className="graph-legend">
          <span className="legend-item"><span className="legend-dot plumb" /> Baseline</span>
          <span className="legend-item"><span className="legend-dot holds" /> Preserved</span>
          <span className="legend-item"><span className="legend-dot drift" /> Diverged</span>
        </span>
        <button
          className="view-toggle-btn"
          onClick={() => setShowTable(true)}
          title="Switch to accessible tabular view"
        >
          Show as Table
        </button>
      </div>

      <div className="plumb-svg-container">
        <svg
          width={width}
          height={height}
          viewBox={`0 0 ${width} ${height}`}
          role="img"
          aria-label={ariaSummary}
          className="plumb-svg"
        >
          {/* Subtle grid and vertical plumb guideline */}
          <line
            x1={layout.baselineX}
            y1={layout.anchor.y}
            x2={layout.baselineX}
            y2={layout.baselineEndY}
            className="plumb-guideline"
          />

          {/* Anchor top mark */}
          <g className="plumb-anchor-group">
            <rect
              x={layout.anchor.x - 12}
              y={layout.anchor.y - 12}
              width={24}
              height={6}
              rx={3}
              className="plumb-anchor-bracket"
            />
            <circle
              cx={layout.anchor.x}
              cy={layout.anchor.y}
              r={5}
              className="plumb-anchor-dot"
            />
          </g>

          {/* Checkpoints along baseline */}
          {layout.checkpoints.map(cp => {
            const isReached = state.currentStage >= cp.stage;
            return (
              <g key={cp.stage} className={`plumb-checkpoint-group ${isReached ? 'reached' : ''}`}>
                <circle
                  cx={cp.x}
                  cy={cp.y}
                  r={5}
                  className="plumb-checkpoint-dot"
                />
                <text
                  x={cp.x + 14}
                  y={cp.y + 4}
                  className="plumb-checkpoint-label"
                >
                  {cp.label}
                </text>
              </g>
            );
          })}

          {/* Tick strip for planted bugs (Stage 3) */}
          {layout.ticks.length > 0 && (
            <g className="plumb-tick-strip">
              <line
                x1={layout.ticks[0]?.x ? layout.ticks[0].x - 10 : layout.baselineX - 100}
                y1={175}
                x2={layout.ticks[layout.ticks.length - 1]?.x ? layout.ticks[layout.ticks.length - 1]!.x + 10 : layout.baselineX + 100}
                y2={175}
                className="plumb-tick-bar"
              />
              {layout.ticks.map(t => (
                <g key={t.index} className={`plumb-tick tick-${t.status}`}>
                  <line
                    x1={t.x}
                    y1={t.y - 6}
                    x2={t.x}
                    y2={t.y + 6}
                    className="tick-line"
                  />
                  {t.status === 'caught' ? (
                    <circle cx={t.x} cy={t.y} r={3} className="tick-dot-caught" />
                  ) : (
                    <circle cx={t.x} cy={t.y} r={3} className="tick-dot-survived" />
                  )}
                </g>
              ))}
              <text x={layout.baselineX} y={198} textAnchor="middle" className="plumb-tick-caption">
                Planted bugs (tripwires): {layout.ticks.filter(t => t.status === 'caught').length}/{layout.ticks.length} caught
              </text>
            </g>
          )}

          {/* Candidate cables and bobs (Stage 4 - 6) */}
          {layout.candidates.map((c, i) => {
            const isWinner = c.isWinner;
            const isDimmed = state.verdict && !isWinner;
            const isHovered = hoveredCandidate === c.id;
            const candidateLetter = String.fromCharCode(65 + i); // A, B, C...

            return (
              <g
                key={c.id}
                className={`plumb-candidate ${isWinner ? 'winner' : ''} ${isDimmed ? 'dimmed' : ''} ${isHovered ? 'hovered' : ''}`}
                onClick={() => onCandidateSelect?.(c.id)}
                onMouseEnter={() => setHoveredCandidate(c.id)}
                onMouseLeave={() => setHoveredCandidate(null)}
                tabIndex={0}
                role="button"
                aria-label={`Candidate ${candidateLetter}: drift ${c.drift.toFixed(2)}, status ${c.status}`}
              >
                {/* Cable line: split into normal and drift segments if divergence exists */}
                {c.divergencePoint ? (
                  <>
                    <line
                      x1={c.cableStart.x}
                      y1={c.cableStart.y}
                      x2={c.divergencePoint.x}
                      y2={c.divergencePoint.y}
                      className="plumb-cable base"
                    />
                    <line
                      x1={c.divergencePoint.x}
                      y1={c.divergencePoint.y}
                      x2={c.cableEnd.x}
                      y2={c.cableEnd.y}
                      className="plumb-cable drift"
                    />
                    {/* Divergence indicator badge */}
                    <circle
                      cx={c.divergencePoint.x}
                      cy={c.divergencePoint.y}
                      r={3.5}
                      className="drift-point"
                    />
                  </>
                ) : (
                  <line
                    x1={c.cableStart.x}
                    y1={c.cableStart.y}
                    x2={c.cableEnd.x}
                    y2={c.cableEnd.y}
                    className="plumb-cable base"
                  />
                )}

                {/* Candidate Bob */}
                <g className="plumb-bob-group">
                  <circle
                    cx={c.cableEnd.x}
                    cy={c.cableEnd.y}
                    r={13}
                    className="plumb-bob-outer"
                  />
                  <text
                    x={c.cableEnd.x}
                    y={c.cableEnd.y + 4}
                    textAnchor="middle"
                    className="plumb-bob-text"
                  >
                    {candidateLetter}
                  </text>
                  <text
                    x={c.cableEnd.x}
                    y={c.cableEnd.y + 24}
                    textAnchor="middle"
                    className="plumb-bob-label"
                  >
                    {c.drift === 0 ? 'Drift 0.0' : `Drift +${c.drift.toFixed(2)}`}
                  </text>
                </g>
              </g>
            );
          })}
        </svg>

        {/* Hover Telemetry Card */}
        {activeCandidateData && (
          <div className="candidate-telemetry-popover">
            <div className="telemetry-header">
              <span className="telemetry-title">Candidate Telemetry</span>
              <span className={`telemetry-badge ${activeCandidateData.drift === 0 ? 'holds' : 'diverged'}`}>
                {activeCandidateData.drift === 0 ? 'Invariant Preserved' : 'Drift Detected'}
              </span>
            </div>
            <div className="telemetry-grid">
              <div className="telemetry-stat">
                <span className="stat-label">Strategy</span>
                <span className="stat-val">{activeCandidateData.name || 'Conservative'}</span>
              </div>
              <div className="telemetry-stat">
                <span className="stat-label">Drift Metric</span>
                <span className="stat-val">{activeCandidateData.drift.toFixed(3)}</span>
              </div>
              <div className="telemetry-stat">
                <span className="stat-label">Deflection Angle</span>
                <span className="stat-val">{(activeCandidateData.drift * 30).toFixed(1)}°</span>
              </div>
              <div className="telemetry-stat">
                <span className="stat-label">Differential Probes</span>
                <span className="stat-val">
                  {activeCandidateData.drift === 0 ? '50/50 Matching' : '7/50 Divergent'}
                </span>
              </div>
            </div>
          </div>
        )}

        {/* Verdict sentence rendered beneath graph */}
        {state.verdict && (
          <div className={`plumb-verdict-banner ${state.verdict}`}>
            <span className="verdict-icon">{state.verdict === 'held' ? '✓' : '✗'}</span>
            <span className="verdict-text">
              {state.verdictSentence ||
                (state.verdict === 'held'
                  ? 'Verdict: Candidate A held true. No behavioral divergence detected.'
                  : 'Verdict: Behavioral drift detected across differential probes.')}
            </span>
          </div>
        )}
      </div>
    </div>
  );
}
