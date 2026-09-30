import { useEffect, useRef } from 'react';
import './CockpitScreen.css';
import { useRunStream } from '../lib/useRunStream';
import StatusPill from '../components/StatusPill';
import StageRow from '../components/StageRow';
import PlumbGraph from '../graph/PlumbGraph';
import Button from '../components/Button';
import TestStrengthMeter from '../components/TestStrengthMeter';
import { cancelRun } from '../lib/api';

interface CockpitScreenProps {
  runId: string;
}

export default function CockpitScreen({ runId }: CockpitScreenProps) {
  const { state, error } = useRunStream(runId);
  const logsEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    logsEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [state.logs]);

  const handleCancel = async () => {
    try {
      await cancelRun(runId);
    } catch (e) {
      console.error('Cancel failed:', e);
    }
  };

  if (error) {
    return (
      <div className="cockpit-error">
        <h3>Connection error</h3>
        <p>{error.message}</p>
        <Button variant="secondary" onClick={() => window.location.hash = '#/'}>
          Back to Home
        </Button>
      </div>
    );
  }

  const stages = [
    { num: 1, name: 'Read the code' },
    { num: 2, name: 'Record behavior' },
    { num: 3, name: 'Plant bugs to test the tests' },
    { num: 4, name: 'Try refactors' },
    { num: 5, name: 'Compare with the original' },
    { num: 6, name: 'Write the dossier' },
  ];

  const caught = state.mutants.filter(m => m === 'caught').length;
  const survived = state.mutants.filter(m => m === 'survived').length;
  const timeout = state.mutants.filter(m => m === 'timeout').length;

  return (
    <div className="cockpit-screen">
      <header className="cockpit-header">
        <div className="header-left">
          <button className="back-link" onClick={() => window.location.hash = '#/'}>
            ← Back
          </button>
          <div className="cockpit-title">Run: <code>{runId.slice(0, 12)}...</code></div>
          <StatusPill status={state.status as any} label={state.status} />
        </div>
        <div className="cockpit-actions">
          {state.status === 'completed' ? (
            <Button
              variant="primary"
              onClick={() => window.location.hash = `#/dossier/${runId}`}
            >
              View Dossier →
            </Button>
          ) : state.status === 'running' ? (
            <Button variant="quiet" onClick={handleCancel}>
              Cancel run
            </Button>
          ) : null}
        </div>
      </header>

      <div className="cockpit-body">
        <aside className="cockpit-rail">
          <div className="rail-heading">Stages</div>
          {stages.map(s => (
            <StageRow
              key={s.num}
              number={s.num}
              name={s.name}
              status={state.stages[s.num] || 'pending'}
            />
          ))}

          {state.mutants.length > 0 && (
            <div className="strength-widget">
              <div className="widget-label">Test strength (planted bugs)</div>
              <TestStrengthMeter caught={caught} survived={survived} timeout={timeout} />
              <div className="strength-sub">
                {caught} caught, {survived} survived
              </div>
            </div>
          )}
        </aside>

        <main className="cockpit-center">
          <div className="graph-card">
            <div className="graph-title">Plumb Graph</div>
            <p className="graph-sub">Vertical baseline represents true behavior. Deviation indicates behavioral drift.</p>
            <PlumbGraph state={state} width={600} height={420} />
          </div>
        </main>

        <aside className="cockpit-panel">
          <div className="panel-tabs">
            <span className="panel-tab active">Event stream</span>
          </div>
          <div className="logs-container">
            {state.logs.map((l, i) => (
              <div key={i} className="log-line">
                <span className="log-bullet">•</span> {l}
              </div>
            ))}
            <div ref={logsEndRef} />
          </div>
        </aside>
      </div>
    </div>
  );
}
