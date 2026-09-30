import { RunState } from '../lib/types';

export interface TickLayout {
  index: number;
  x: number;
  y: number;
  status: 'caught' | 'survived' | 'timeout' | 'error';
}

export interface CandidateLayout {
  id: string;
  name: string;
  status: string;
  drift: number;
  angleDeg: number;
  isWinner: boolean;
  cableStart: { x: number; y: number };
  cableEnd: { x: number; y: number };
  divergencePoint?: { x: number; y: number };
}

export interface GraphLayout {
  width: number;
  height: number;
  anchor: { x: number; y: number };
  baselineX: number;
  baselineEndY: number;
  checkpoints: Array<{ x: number; y: number; stage: number; label: string }>;
  ticks: TickLayout[];
  candidates: CandidateLayout[];
}

export function computeGraphLayout(state: RunState, width: number = 600, height: number = 460): GraphLayout {
  const centerX = width / 2;
  const baselineX = centerX;
  const anchor = { x: centerX, y: 24 };

  const checkpoints = [
    { x: centerX, y: 70, stage: 2, label: 'Behavior recorded' },
    { x: centerX, y: 130, stage: 3, label: 'Tests strengthened' },
    { x: centerX, y: 220, stage: 4, label: 'Try refactors' },
  ];

  // Tick strip for planted bugs (placed between stage 3 and 4)
  const ticks: TickLayout[] = [];
  const mutants = state.mutants || [];
  const tickCount = mutants.length;
  if (tickCount > 0) {
    const stripWidth = Math.min(width * 0.75, 420);
    const startX = centerX - stripWidth / 2;
    const step = tickCount > 1 ? stripWidth / (tickCount - 1) : 0;
    const tickY = 175;

    mutants.forEach((m, idx) => {
      ticks.push({
        index: idx + 1,
        x: tickCount === 1 ? centerX : startX + idx * step,
        y: tickY,
        status: m,
      });
    });
  }

  // Candidate cables hanging from checkpoint 3 (Stage 4)
  const cableStart = { x: centerX, y: 220 };
  const cableLength = Math.min(height - 260, 180);

  const candidates: CandidateLayout[] = (state.candidates || []).map((c, idx) => {
    const isWinner = state.verdict === 'held' && (state.winner_id ? c.id === state.winner_id : c.drift === 0);
    
    // Angle calculation: drift * 30 capped between 0 and 30 deg
    // Winner settles straight (0 deg) when verdict is reached
    let angleDeg = 0;
    if (isWinner && state.verdict) {
      angleDeg = 0;
    } else if (c.drift > 0) {
      // Alternate left/right swings with minimum 18 deg for clean visual separation
      const sign = idx % 2 === 1 ? 1 : -1;
      const magnitude = Math.max(18, Math.min(32, 14 + c.drift * 60));
      angleDeg = sign * magnitude;
    } else if (idx > 0 && !isWinner) {
      angleDeg = idx % 2 === 1 ? 18 : -18;
    }

    const rad = angleDeg * (Math.PI / 180);
    const endX = centerX + Math.sin(rad) * cableLength;
    const endY = cableStart.y + Math.cos(rad) * cableLength;

    let divergencePoint: { x: number; y: number } | undefined;
    if (c.drift > 0) {
      // Divergence point 45% along the cable where behavior diverged
      divergencePoint = {
        x: centerX + Math.sin(rad) * (cableLength * 0.45),
        y: cableStart.y + Math.cos(rad) * (cableLength * 0.45),
      };
    }

    return {
      id: c.id,
      name: c.name || c.id,
      status: c.status,
      drift: c.drift,
      angleDeg,
      isWinner,
      cableStart,
      cableEnd: { x: endX, y: endY },
      divergencePoint,
    };
  });

  return {
    width,
    height,
    anchor,
    baselineX,
    baselineEndY: height - 30,
    checkpoints,
    ticks,
    candidates,
  };
}
