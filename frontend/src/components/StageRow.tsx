import React from 'react';
import './StageRow.css';
import { StageStatus } from '../lib/types';
import { Check, Loader2, AlertTriangle } from 'lucide-react';

interface StageRowProps {
  number: number;
  name: string;
  status: StageStatus;
  elapsedTime?: string;
  resultLine?: string;
}

export default function StageRow({ number, name, status, elapsedTime, resultLine }: StageRowProps) {
  let icon;
  if (status === 'completed') icon = <Check size={16} />;
  else if (status === 'running') icon = <Loader2 size={16} className="stage-spinner" />;
  else if (status === 'failed') icon = <AlertTriangle size={16} />;
  else icon = <div className="stage-pending-dot" />;

  return (
    <div className={`stage-row stage-${status}`}>
      <div className="stage-header">
        <span className="stage-number">{number}</span>
        <span className="stage-name">{name}</span>
        <span className="stage-icon">{icon}</span>
        {elapsedTime && <span className="stage-time">{elapsedTime}</span>}
      </div>
      {resultLine && <div className="stage-result">{resultLine}</div>}
    </div>
  );
}
