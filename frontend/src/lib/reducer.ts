import { RunState, EventEnvelope } from './types';

export const initialState: RunState = {
  id: null,
  status: 'queued',
  currentStage: 1,
  stages: {
    1: 'pending',
    2: 'pending',
    3: 'pending',
    4: 'pending',
    5: 'pending',
    6: 'pending'
  },
  candidates: [],
  mutants: [],
  verdict: null,
  logs: [],
  ledger: [],
  dossier: null,
};

export function reduceEvent(state: RunState, event: EventEnvelope): RunState {
  switch (event.type) {
    case 'RunStarted':
      return { ...state, status: 'running', id: event.data.runId };
    case 'StageStarted':
      return {
        ...state,
        currentStage: event.data.stage,
        stages: { ...state.stages, [event.data.stage]: 'running' }
      };
    case 'StageCompleted':
      return {
        ...state,
        stages: { ...state.stages, [event.data.stage]: 'completed' }
      };
    case 'Log':
      return { ...state, logs: [...state.logs, event.data.message] };
    case 'RunCompleted':
      return { ...state, status: 'completed', verdict: event.data.verdict };
    case 'RunFailed':
      return { ...state, status: 'failed' };
    default:
      return state;
  }
}
