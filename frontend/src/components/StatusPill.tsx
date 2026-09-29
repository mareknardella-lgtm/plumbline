import React from 'react';
import './StatusPill.css';
import { Check, X, AlertTriangle, Loader2 } from 'lucide-react';

interface StatusPillProps {
  status: 'live' | 'running' | 'completed' | 'failed' | 'cancelled' | 'replay' | 'connecting';
  label: string;
}

export default function StatusPill({ status, label }: StatusPillProps) {
  let icon;
  switch (status) {
    case 'live':
    case 'replay':
      icon = <div className={`status-dot status-dot-${status}`} />;
      break;
    case 'running':
    case 'connecting':
      icon = <Loader2 size={14} className="status-spinner" />;
      break;
    case 'completed':
      icon = <Check size={14} />;
      break;
    case 'failed':
      icon = <AlertTriangle size={14} />;
      break;
    case 'cancelled':
      icon = <X size={14} />;
      break;
  }

  return (
    <div className={`status-pill status-${status}`}>
      {icon}
      <span>{label}</span>
    </div>
  );
}
