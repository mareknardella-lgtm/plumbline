import { describe, it, expect } from 'vitest';
import { computeGraphLayout } from '../graph/geometry';

describe('geometry', () => {
  it('should compute basic layout without candidates', () => {
    const layout = computeGraphLayout({ candidates: [], mutants: [] } as any, 500, 500);
    expect(layout.anchor).toEqual({ x: 250, y: 24 });
    expect(layout.baselineX).toBe(250);
    expect(layout.checkpoints).toHaveLength(3);
    expect(layout.candidates).toHaveLength(0);
    expect(layout.ticks).toHaveLength(0);
  });

  it('should compute candidate swing angles based on drift', () => {
    const state = {
      candidates: [
        { id: 'cand-cons', name: 'conservative', status: 'completed', drift: 0 },
        { id: 'cand-bal', name: 'balanced', status: 'completed', drift: 0.15 },
      ],
      mutants: ['caught', 'caught', 'survived'],
      verdict: null,
    } as any;

    const layout = computeGraphLayout(state, 600, 460);
    expect(layout.ticks).toHaveLength(3);
    expect(layout.candidates).toHaveLength(2);

    const candA = layout.candidates[0]!;
    const candB = layout.candidates[1]!;

    expect(candA.drift).toBe(0);
    expect(candB.drift).toBe(0.15);
    expect(candB.angleDeg).not.toBe(0);
    expect(candB.divergencePoint).toBeDefined();
  });

  it('should settle winner straight down when verdict holds', () => {
    const state = {
      candidates: [
        { id: 'cand-cons', name: 'conservative', status: 'completed', drift: 0 },
        { id: 'cand-bal', name: 'balanced', status: 'completed', drift: 0.15 },
      ],
      mutants: ['caught'],
      verdict: 'held',
    } as any;

    const layout = computeGraphLayout(state, 600, 460);
    const winner = layout.candidates.find(c => c.isWinner);
    expect(winner).toBeDefined();
    expect(winner?.angleDeg).toBe(0);
  });
});
