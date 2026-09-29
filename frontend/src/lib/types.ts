export type RunStatus = 'queued' | 'running' | 'completed' | 'failed' | 'cancelled';
export type StageStatus = 'pending' | 'running' | 'completed' | 'failed';
export type VerdictOutcome = 'held' | 'dropped' | 'error';
export type MutantResultStatus = 'caught' | 'survived' | 'timeout' | 'error';

export interface EventEnvelope {
  seq: number;
  type: string;
  timestamp: string;
  data: any;
}

export interface RunStartedData {
  runId: string;
  specimenId: string;
}

export interface CandidateStrategy {
  id: string;
  name: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  drift: number;
}

export interface SpecimenInfo {
  id: string;
  name: string;
  description: string;
}

export interface ReplayInfo {
  id: string;
  originalRunId: string;
  recordedAt: string;
}

export interface RunState {
  id: string | null;
  status: RunStatus;
  currentStage: number;
  stages: Record<number, StageStatus>;
  candidates: CandidateStrategy[];
  mutants: MutantResultStatus[];
  verdict: VerdictOutcome | null;
  logs: string[];
  ledger: any[];
  dossier: any | null;
}
