import { RunState } from '../lib/types';

export interface GraphLayout {
  width: number;
  height: number;
  anchor: { x: number; y: number };
  baselineX: number;
  checkpoints: Array<{ x: number; y: number; stage: number }>;
  candidates: Array<{ id: string; points: Array<{ x: number; y: number }>; driftAngle: number }>;
}

export function computeGraphLayout(state: RunState, width: number, height: number): GraphLayout {
  const centerX = width / 2;
  const baselineX = centerX;
  const anchor = { x: centerX, y: 20 };
  
  const checkpoints = [
    { x: centerX, y: height * 0.3, stage: 2 },
    { x: centerX, y: height * 0.6, stage: 3 },
    { x: centerX, y: height * 0.9, stage: 4 }
  ];

  const candidates = state.candidates.map(c => {
    const driftAngle = Math.max(0, Math.min(c.drift * 30, 30)); // clamp 0-30
    const rad = driftAngle * (Math.PI / 180);
    const length = height * 0.4;
    const endX = centerX + Math.sin(rad) * length;
    const endY = height * 0.9 + Math.cos(rad) * length;
    
    const startPoint = { x: checkpoints[2]?.x ?? centerX, y: checkpoints[2]?.y ?? height * 0.9 };
    return {
      id: c.id,
      driftAngle,
      points: [
        startPoint,
        { x: endX, y: endY }
      ]
    };
  });

  return { width, height, anchor, baselineX, checkpoints, candidates };
}
