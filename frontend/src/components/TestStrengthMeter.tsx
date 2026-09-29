import React from 'react';
import './TestStrengthMeter.css';

interface TestStrengthMeterProps {
  caught: number;
  survived: number;
  timeout: number;
}

export default function TestStrengthMeter({ caught, survived, timeout }: TestStrengthMeterProps) {
  const total = caught + survived + timeout;
  if (total === 0) return null;

  const getTicks = () => {
    const ticks: string[] = [];
    for (let i = 0; i < caught; i++) ticks.push('caught');
    for(let i=0; i<survived; i++) ticks.push('survived');
    for(let i=0; i<timeout; i++) ticks.push('timeout');
    return ticks;
  };

  return (
    <div className="test-meter" aria-label={`Test strength: ${caught} caught, ${survived} survived, ${timeout} timeout`}>
      <div className="test-meter-line" />
      <div className="test-meter-ticks">
        {getTicks().map((type, i) => (
          <div key={i} className={`test-tick tick-${type}`} />
        ))}
      </div>
    </div>
  );
}
