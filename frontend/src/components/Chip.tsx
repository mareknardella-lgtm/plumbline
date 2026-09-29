import React from 'react';
import './Chip.css';

interface ChipProps {
  label: string;
  selected?: boolean;
  onClick?: () => void;
}

export default function Chip({ label, selected = false, onClick }: ChipProps) {
  return (
    <button 
      className={`chip ${selected ? 'chip-selected' : ''}`}
      onClick={onClick}
      aria-pressed={selected}
    >
      {label}
    </button>
  );
}
