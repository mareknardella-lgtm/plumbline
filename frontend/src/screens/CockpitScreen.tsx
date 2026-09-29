import React from 'react';
import './CockpitScreen.css';
import { useRunStream } from '../lib/useRunStream';
import StatusPill from '../components/StatusPill';
import StageRow from '../components/StageRow';
import PlumbGraph from '../graph/PlumbGraph';
import Button from '../components/Button';

interface CockpitScreenProps {
  runId: string;
}

export default function CockpitScreen({ runId }: CockpitScreenProps) {
  const { state, error, isConnected } = useRunStream(runId);

  const handleCancel = () => {
    // API call to cancel
  };

  if (error) {
    return <div className="cockpit-error">Failed to connect: {error.message}</div>;
  }

  const stages = [
    { num: 1, name: 'Initialization' },
    { num: 2, name: 'Analysis' },
    { num: 3, name: 'Generation' },
    { num: 4, name: 'Testing' },
    { num: 5, name: 'Evaluation' },
    { num: 6, name: 'Finalization' },
  ];

  return (
    <div className="cockpit-screen">
      <header className="cockpit-header">
        <div className="cockpit-title">Run: {runId}</div>
        <StatusPill status={state.status as any} label={state.status} />
        <div className="cockpit-actions">
          <Button variant="quiet" onClick={handleCancel}>Cancel</Button>
        </div>
      </header>

      <div className="cockpit-body">
        <aside className="cockpit-rail">
          {stages.map(s => (
            <StageRow 
              key={s.num}
              number={s.num} 
              name={s.name} 
              status={state.stages[s.num] || 'pending'} 
            />
          ))}
        </aside>
        
        <main className="cockpit-center">
          <PlumbGraph state={state} width={600} height={500} />
        </main>
        
        <aside className="cockpit-panel">
          <h3>Logs</h3>
          <div className="logs-container">
            {state.logs.map((l, i) => <div key={i} className="log-line">{l}</div>)}
          </div>
        </aside>
      </div>
    </div>
  );
}
