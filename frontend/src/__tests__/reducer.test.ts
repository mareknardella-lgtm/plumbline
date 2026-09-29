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
});
