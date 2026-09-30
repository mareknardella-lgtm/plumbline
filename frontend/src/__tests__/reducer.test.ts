import { describe, it, expect } from 'vitest';
import { reduceEvent, initialState } from '../lib/reducer';

describe('reducer', () => {
  it('should handle RunStarted', () => {
    const state = reduceEvent(initialState, {
      seq: 1,
      type: 'RunStarted',
      timestamp: new Date().toISOString(),
      data: { runId: 'run-123' }
    });
    expect(state.status).toBe('running');
    expect(state.id).toBe('run-123');
  });

  it('should handle StageStarted', () => {
    const state = reduceEvent(initialState, {
      seq: 2,
      type: 'StageStarted',
      timestamp: new Date().toISOString(),
      data: { stage: 2 }
    });
    expect(state.currentStage).toBe(2);
    expect(state.stages[2]).toBe('running');
  });

  it('should handle llm.call and populate ledger', () => {
    const state = reduceEvent(initialState, {
      seq: 3,
      type: 'llm.call',
      timestamp: new Date().toISOString(),
      data: {
        model: 'nvidia/nemotron-3-super-120b-a12b',
        tier: 'super',
        tokens_in: 500,
        tokens_out: 120,
        latency_ms: 340,
        cost_estimate_usd: 0.0025,
      }
    });
    expect(state.ledger.length).toBe(1);
    expect(state.ledger[0].tier).toBe('super');
    expect(state.ledger[0].tokens_in).toBe(500);
  });
});
