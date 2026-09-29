import React from 'react';
import './SegmentedControl.css';

interface SegmentedControlProps {
  options: { label: string; value: string }[];
  value: string;
  onChange: (val: string) => void;
  ariaLabel?: string;
}

export default function SegmentedControl({ options, value, onChange, ariaLabel }: SegmentedControlProps) {
  return (
    <div className="segmented-control" role="group" aria-label={ariaLabel}>
      {options.map((opt) => (
        <button
          key={opt.value}
          className={`segment ${value === opt.value ? 'segment-active' : ''}`}
          onClick={() => onChange(opt.value)}
          aria-pressed={value === opt.value}
        >
          {opt.label}
        </button>
      ))}
    </div>
  );
}
