import { RunState, EventEnvelope, CandidateStrategy } from './types';

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
    6: 'pending',
  },
  candidates: [],
  mutants: [],
  verdict: null,
  logs: [],
  ledger: [],
  dossier: null,
};

export function reduceEvent(state: RunState, event: EventEnvelope): RunState {
  const t = event.type.toLowerCase().replace('_', '.');
  const d = event.data || {};

  switch (t) {
    case 'run.started':
    case 'runstarted':
      return {
        ...state,
        status: 'running',
        id: d.run_id || d.runId || state.id,
        logs: [...state.logs, `Run started in ${d.mode || 'quick'} mode`],
      };

    case 'stage.started':
    case 'stagestarted': {
      const stage = d.stage || 1;
      return {
        ...state,
        currentStage: stage,
        stages: { ...state.stages, [stage]: 'running' },
        logs: [...state.logs, `Stage ${stage} started: ${d.name || ''}`],
      };
    }

    case 'stage.completed':
    case 'stagecompleted': {
      const stage = d.stage || state.currentStage;
      return {
        ...state,
        stages: { ...state.stages, [stage]: 'completed' },
        logs: [...state.logs, `Stage ${stage} completed (${d.elapsed_seconds || 0}s): ${d.summary || ''}`],
      };
    }

    case 'survey.report':
      return {
        ...state,
        logs: [...state.logs, `Survey report: found ${d.functions_found || 0} functions`],
      };

    case 'pins.written':
      return {
        ...state,
        logs: [...state.logs, `Wrote ${d.count || 0} behavior tests (${d.coverage_percent || 0}% coverage)`],
      };

    case 'mutants.planned':
      return {
        ...state,
        logs: [...state.logs, `Planned ${d.total || 0} planted bugs (mutants)`],
      };

    case 'mutant.result': {
      const status = d.status || 'caught';
      return {
        ...state,
        mutants: [...state.mutants, status],
        logs: [...state.logs, `Planted bug #${d.index || 0} (${d.function_name || ''}): ${status}`],
      };
    }

    case 'test_strength.updated':
      return {
        ...state,
        logs: [...state.logs, `Test strength: ${d.test_strength} (${d.caught}/${d.total} caught)`],
      };

    case 'candidate.started': {
      const candId = d.candidate_id || d.candidateId || 'cand';
      const strategyName = d.strategy || 'candidate';
      const existing = state.candidates.find(c => c.id === candId);
      const updated: CandidateStrategy = existing || {
        id: candId,
        name: strategyName,
        status: 'running',
        drift: 0,
      };
      return {
        ...state,
        candidates: existing ? state.candidates : [...state.candidates, updated],
        logs: [...state.logs, `Candidate ${candId} (${strategyName}) started`],
      };
    }

    case 'candidate.iteration':
      return {
        ...state,
        logs: [...state.logs, `Candidate ${d.candidate_id}: iteration ${d.iteration} - ${d.action || ''}`],
      };

    case 'candidate.result': {
      const candId = d.candidate_id || d.candidateId;
      const status = d.status === 'green' ? 'completed' : 'failed';
      return {
        ...state,
        candidates: state.candidates.map(c =>
          c.id === candId ? { ...c, status } : c
        ),
        logs: [...state.logs, `Candidate ${candId} finished: ${d.status} (${d.tests_passed}/${d.tests_total} tests)`],
      };
    }

    case 'probe.result': {
      const candId = d.candidate_id;
      const total = d.total_probes || 1;
      const div = d.divergent || 0;
      const drift = div / total;
      return {
        ...state,
        candidates: state.candidates.map(c =>
          c.id === candId ? { ...c, drift } : c
        ),
        logs: [
          ...state.logs,
          `Probes for ${candId}: ${d.matching}/${total} matching, ${div} divergent`,
        ],
      };
    }

    case 'verdict':
      return {
        ...state,
        verdict: d.outcome === 'holds' ? 'held' : 'dropped',
        logs: [...state.logs, `Verdict: ${d.outcome?.toUpperCase() || ''} - ${d.sentence || ''}`],
      };

    case 'dossier.ready':
      return {
        ...state,
        dossier: d,
        logs: [...state.logs, `Dossier ready with artifacts: ${(d.artifacts || []).join(', ')}`],
      };

    case 'run.completed':
    case 'runcompleted':
      return {
        ...state,
        status: 'completed',
        logs: [...state.logs, `Run completed in ${d.duration_seconds || 0}s`],
      };

    case 'run.failed':
    case 'runfailed':
      return {
        ...state,
        status: 'failed',
        logs: [...state.logs, `Run failed: ${d.reason || ''}`],
      };

    case 'run.cancelled':
    case 'runcancelled':
      return {
        ...state,
        status: 'cancelled',
        logs: [...state.logs, `Run cancelled: ${d.reason || ''}`],
      };

    case 'log':
      return { ...state, logs: [...state.logs, d.message || ''] };

    default:
      return state;
  }
}
