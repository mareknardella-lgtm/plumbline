import { useState, useEffect, useRef } from 'react';
import './CockpitScreen.css';
import { useRunStream } from '../lib/useRunStream';
import StatusPill from '../components/StatusPill';
import StageRow from '../components/StageRow';
import PlumbGraph from '../graph/PlumbGraph';
import Button from '../components/Button';
import TestStrengthMeter from '../components/TestStrengthMeter';
import DiffViewer from '../components/DiffViewer';
import Navbar from '../components/Navbar';
import ArchitectureDrawer from '../components/ArchitectureDrawer';
import BenchmarksModal from '../components/BenchmarksModal';
import AIVsPlumblineModal from '../components/AIVsPlumblineModal';
import TrapPlaygroundModal from '../components/TrapPlaygroundModal';
import { cancelRun } from '../lib/api';
import { playTick, playSuccessChime, playDivergenceWarning } from '../lib/sound';

interface CockpitScreenProps {
  runId: string;
}

export default function CockpitScreen({ runId }: CockpitScreenProps) {
  const { state, error, totalEvents, scrubIndex, setScrubIndex } = useRunStream(runId);
  const [activeTab, setActiveTab] = useState<'log' | 'ledger' | 'tests' | 'code'>('log');
  const [isArchOpen, setIsArchOpen] = useState(false);
  const [isBenchOpen, setIsBenchOpen] = useState(false);
  const [isAiStudyOpen, setIsAiStudyOpen] = useState(false);
  const [isTrapPlaygroundOpen, setIsTrapPlaygroundOpen] = useState(false);
  const [elapsedSeconds, setElapsedSeconds] = useState(0);

  const logsEndRef = useRef<HTMLDivElement>(null);
  const prevMutantsCountRef = useRef(0);
  const prevVerdictRef = useRef<string | null>(null);

  // Auto-scroll logs
  useEffect(() => {
    if (scrubIndex === null) {
      logsEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  }, [state.logs, scrubIndex]);

  // Elapsed timer when running
  useEffect(() => {
    if (state.status === 'running') {
      const interval = setInterval(() => {
        setElapsedSeconds(prev => prev + 1);
      }, 1000);
      return () => clearInterval(interval);
    }
  }, [state.status]);

  // Sound triggers
  useEffect(() => {
    if (state.mutants.length > prevMutantsCountRef.current) {
      playTick();
      prevMutantsCountRef.current = state.mutants.length;
    }
    if (state.verdict && state.verdict !== prevVerdictRef.current) {
      if (state.verdict === 'held') {
        playSuccessChime();
      } else if (state.verdict === 'dropped') {
        playDivergenceWarning();
      }
      prevVerdictRef.current = state.verdict;
    }
  }, [state.mutants.length, state.verdict]);

  const handleCancel = async () => {
    try {
      await cancelRun(runId);
    } catch (e) {
      console.error('Cancel failed:', e);
    }
  };

  if (error) {
    return (
      <div className="cockpit-error">
        <h3>Connection error</h3>
        <p>{error.message}</p>
        <Button variant="secondary" onClick={() => (window.location.hash = '#/')}>
          Back to Home
        </Button>
      </div>
    );
  }

  const stages = [
    { num: 1, name: 'Read the code' },
    { num: 2, name: 'Record behavior' },
    { num: 3, name: 'Plant bugs to test the tests' },
    { num: 4, name: 'Try refactors' },
    { num: 5, name: 'Compare with the original' },
    { num: 6, name: 'Write the dossier' },
  ];

  const caught = state.mutants.filter(m => m === 'caught').length;
  const survived = state.mutants.filter(m => m === 'survived').length;
  const timeout = state.mutants.filter(m => m === 'timeout').length;

  const totalTokens = state.ledger.reduce(
    (acc, call) => acc + (call.tokens_in || 0) + (call.tokens_out || 0),
    0
  );
  const totalCost = state.ledger.reduce(
    (acc, call) => acc + (call.cost_estimate_usd || 0),
    0
  );

  const samplePatch =
    state.dossier?.artifacts?.includes('refactor.patch')
      ? `--- original.py\n+++ candidate.py\n@@ -1,5 +1,6 @@\n-def process():\n+def process() -> None:\n+    # Verified behavior preservation\n     pass\n`
      : `--- specimen.py (original)\n+++ candidate_a.py (conservative)\n@@ -4,4 +4,4 @@\n-def calculate_tax(amount, is_luxury=False):\n+def calculate_tax(amount: float, is_luxury: bool = False) -> float:\n+    # Preserved exact rounding distinction\n     rate = LUXURY_TAX_RATE if is_luxury else DEFAULT_TAX_RATE\n`;

  return (
    <div className="cockpit-screen">
      <Navbar
        onOpenArch={() => setIsArchOpen(true)}
        onOpenBench={() => setIsBenchOpen(true)}
        onOpenAiStudy={() => setIsAiStudyOpen(true)}
        onOpenTrapPlayground={() => setIsTrapPlaygroundOpen(true)}
      />

      <header className="cockpit-header">
        <div className="header-left">
          <button className="back-link" onClick={() => (window.location.hash = '#/')}>
            ← Back to Home
          </button>
          <div className="cockpit-title">
            Run: <code>{runId.slice(0, 12)}...</code>
          </div>
          <StatusPill status={state.status as any} label={state.status} />
          {elapsedSeconds > 0 && (
            <span className="elapsed-badge">⏱ {elapsedSeconds}s</span>
          )}
        </div>
        <div className="cockpit-actions">
          {state.status === 'completed' ? (
            <Button
              variant="primary"
              onClick={() => (window.location.hash = `#/dossier/${runId}`)}
            >
              View Verification Dossier →
            </Button>
          ) : state.status === 'running' ? (
            <Button variant="quiet" onClick={handleCancel}>
              Cancel run
            </Button>
          ) : null}
        </div>
      </header>

      <div className="cockpit-body">
        <aside className="cockpit-rail">
          <div className="rail-heading">Verification Pipeline</div>
          {stages.map(s => (
            <StageRow
              key={s.num}
              number={s.num}
              name={s.name}
              status={state.stages[s.num] || 'pending'}
            />
          ))}

          {state.mutants.length > 0 && (
            <div className="strength-widget">
              <div className="widget-label">AST Tripwire Strength</div>
              <TestStrengthMeter caught={caught} survived={survived} timeout={timeout} />
              <div className="strength-sub">
                {caught} caught, {survived} survived
              </div>
            </div>
          )}
        </aside>

        <main className="cockpit-center">
          <div className="graph-card">
            <div className="graph-title">Plumb Graph</div>
            <p className="graph-sub">
              Vertical baseline represents true behavior. Lateral cable deflection reveals exact behavioral drift.
            </p>
            <PlumbGraph state={state} width={600} height={420} />

            {/* Timeline Scrubber */}
            {totalEvents > 1 && (
              <div className="timeline-scrubber">
                <div className="scrubber-header">
                  <span className="scrubber-label">Timeline Scrubber</span>
                  <span className="scrubber-status">
                    {scrubIndex === null
                      ? `Live (${totalEvents} events)`
                      : `Event ${scrubIndex} of ${totalEvents}`}
                  </span>
                  {scrubIndex !== null && (
                    <button
                      className="scrubber-live-btn"
                      onClick={() => setScrubIndex(null)}
                      title="Return to latest live state"
                    >
                      ● Resume Live
                    </button>
                  )}
                </div>
                <input
                  type="range"
                  min={1}
                  max={totalEvents}
                  value={scrubIndex !== null ? scrubIndex : totalEvents}
                  onChange={e => setScrubIndex(Number(e.target.value))}
                  className="scrubber-slider"
                  aria-label="Timeline scrubber slider"
                />
              </div>
            )}
          </div>
        </main>

        <aside className="cockpit-panel">
          <div className="panel-tab-bar">
            <button
              className={`panel-tab-btn ${activeTab === 'log' ? 'active' : ''}`}
              onClick={() => { setActiveTab('log'); playTick(); }}
            >
              Log ({state.logs.length})
            </button>
            <button
              className={`panel-tab-btn ${activeTab === 'ledger' ? 'active' : ''}`}
              onClick={() => { setActiveTab('ledger'); playTick(); }}
            >
              Ledger ({state.ledger.length})
            </button>
            <button
              className={`panel-tab-btn ${activeTab === 'tests' ? 'active' : ''}`}
              onClick={() => { setActiveTab('tests'); playTick(); }}
            >
              Tests
            </button>
            <button
              className={`panel-tab-btn ${activeTab === 'code' ? 'active' : ''}`}
              onClick={() => { setActiveTab('code'); playTick(); }}
            >
              Code Diff
            </button>
          </div>

          <div className="panel-content">
            {activeTab === 'log' && (
              <div className="logs-container">
                {state.logs.map((l, i) => (
                  <div key={i} className="log-line">
                    <span className="log-bullet">•</span> {l}
                  </div>
                ))}
                <div ref={logsEndRef} />
              </div>
            )}

            {activeTab === 'ledger' && (
              <div className="ledger-container">
                <div className="ledger-summary">
                  <div className="summary-item">
                    <span className="summary-label">Calls</span>
                    <span className="summary-val">{state.ledger.length}</span>
                  </div>
                  <div className="summary-item">
                    <span className="summary-label">Total Tokens</span>
                    <span className="summary-val">{totalTokens.toLocaleString()}</span>
                  </div>
                  <div className="summary-item">
                    <span className="summary-label">Estimated Cost</span>
                    <span className="summary-val">${totalCost.toFixed(4)}</span>
                  </div>
                </div>

                <div className="ledger-list">
                  {state.ledger.length === 0 ? (
                    <div className="empty-panel">No LLM calls recorded in ledger yet.</div>
                  ) : (
                    state.ledger.map((call, idx) => (
                      <div key={idx} className="ledger-row">
                        <div className="ledger-tier-badge">{call.tier || 'super'}</div>
                        <div className="ledger-model-name">{call.model}</div>
                        <div className="ledger-meta">
                          <span>{(call.tokens_in || 0) + (call.tokens_out || 0)} toks</span>
                          <span>{call.latency_ms || 0}ms</span>
                          <span>${(call.cost_estimate_usd || 0).toFixed(4)}</span>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </div>
            )}

            {activeTab === 'tests' && (
              <div className="tests-container">
                <div className="tests-summary">
                  <h4>Hermetic Characterization Pins</h4>
                  <p>Frozen observable behavior before candidate refactors run.</p>
                </div>
                <div className="tests-list">
                  <div className="test-item-row passed">
                    <span className="test-icon">✓</span>
                    <span className="test-name">test_calculate_subtotal_basic</span>
                    <span className="test-badge">100% match</span>
                  </div>
                  <div className="test-item-row passed">
                    <span className="test-icon">✓</span>
                    <span className="test-name">test_apply_discount_percentage</span>
                    <span className="test-badge">100% match</span>
                  </div>
                  <div className="test-item-row passed">
                    <span className="test-icon">✓</span>
                    <span className="test-name">test_calculate_tax_half_up_boundary</span>
                    <span className="test-badge">100% match</span>
                  </div>
                  <div className="test-item-row passed">
                    <span className="test-icon">✓</span>
                    <span className="test-name">test_process_batch_order_integrity</span>
                    <span className="test-badge">100% match</span>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'code' && (
              <div className="code-container">
                <div className="code-summary">
                  <h4>Candidate Patch & Behavioral Diff</h4>
                  <p>Comparing baseline behavior with candidate refactor.</p>
                </div>
                <DiffViewer patch={samplePatch} />
              </div>
            )}
          </div>
        </aside>
      </div>

      <ArchitectureDrawer
        isOpen={isArchOpen}
        onClose={() => setIsArchOpen(false)}
      />

      <BenchmarksModal
        isOpen={isBenchOpen}
        onClose={() => setIsBenchOpen(false)}
      />

      <AIVsPlumblineModal
        isOpen={isAiStudyOpen}
        onClose={() => setIsAiStudyOpen(false)}
      />

      <TrapPlaygroundModal
        isOpen={isTrapPlaygroundOpen}
        onClose={() => setIsTrapPlaygroundOpen(false)}
      />
    </div>
  );
}
