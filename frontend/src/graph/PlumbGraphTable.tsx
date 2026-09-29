import React from 'react';
import Table from '../components/Table';
import { RunState } from '../lib/types';

interface PlumbGraphTableProps {
  state: RunState;
}

export default function PlumbGraphTable({ state }: PlumbGraphTableProps) {
  const headers = ['Candidate ID', 'Status', 'Drift'];
  const rows = state.candidates.map(c => [
    c.id,
    c.status,
    c.drift.toFixed(2)
  ]);

  return (
    <div className="plumb-graph-table">
      <Table headers={headers} rows={rows} />
    </div>
  );
}
