import React, { useState } from 'react';
import './DiffViewer.css';
import SegmentedControl from './SegmentedControl';

interface DiffViewerProps {
  patch: string;
}

export default function DiffViewer({ patch }: DiffViewerProps) {
  const [mode, setMode] = useState('unified');

  return (
    <div className="diff-viewer">
      <div className="diff-header">
        <SegmentedControl 
          options={[{ label: 'Unified', value: 'unified' }, { label: 'Split', value: 'split' }]}
          value={mode}
          onChange={setMode}
        />
      </div>
      <div className={`diff-content diff-${mode}`}>
        <pre>{patch}</pre>
      </div>
    </div>
  );
}
