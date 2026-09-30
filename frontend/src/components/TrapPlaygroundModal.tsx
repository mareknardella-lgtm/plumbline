import React, { useState } from 'react';
import './TrapPlaygroundModal.css';

interface TrapPlaygroundModalProps {
  isOpen: boolean;
  onClose: () => void;
}

interface TrapScenario {
  id: string;
  name: string;
  module: string;
  description: string;
  originalSnippet: string;
  naiveSnippet: string;
  divergentCase: {
    input: string;
    expected: string;
    actual: string;
    delta: string;
  };
}

const SCENARIOS: TrapScenario[] = [
  {
    id: 'rounding',
    name: "Banker's Rounding vs. Half-Up (Penny Drift)",
    module: 'invoice_totals.py',
    description: "Standard LLMs replace manual cent arithmetic with Python's round(). On half-cent values (e.g. 2.505), round() rounds to the nearest even number (2.50), losing 1 cent.",
    originalSnippet: 'def calculate_tax(amount, is_luxury=False):\n    rate = 0.05 if not is_luxury else 0.15\n    tax = amount * rate\n    return int(tax * 100 + 0.5) / 100  # Half-up rounding',
    naiveSnippet: 'def calculate_tax(amount: float, is_luxury: bool = False) -> float:\n    rate = 0.05 if not is_luxury else 0.15\n    return round(amount * rate, 2)  # Banker\'s rounding',
    divergentCase: {
      input: 'amount = 50.10, is_luxury = False (tax = 2.505)',
      expected: '$2.51 (Half-up)',
      actual: '$2.50 (Banker’s rounding)',
      delta: '-$0.01 drift on 7 / 50 test invoices',
    },
  },
  {
    id: 'dict_order',
    name: 'Dictionary Insertion Order & Tie Breaking',
    module: 'log_digester.py',
    description: "Naive refactors use set() to deduplicate log entries, destroying deterministic insertion order and breaking report tie-breakers.",
    originalSnippet: 'def top_errors(events):\n    counts = {}\n    for e in events:\n        counts[e["msg"]] = counts.get(e["msg"], 0) + 1\n    return sorted(counts.items(), key=lambda x: x[1], reverse=True)',
    naiveSnippet: 'def top_errors(events: list[dict]) -> list[tuple]:\n    # "Optimized" with set comprehension\n    unique_msgs = set(e["msg"] for e in events)\n    return sorted([(m, sum(1 for e in events if e["msg"] == m)) for m in unique_msgs], key=lambda x: x[1], reverse=True)',
    divergentCase: {
      input: 'Two error messages with identical frequency (tie = 3)',
      expected: '["Timeout", "ConnectionRefused"] (First-seen order)',
      actual: '["ConnectionRefused", "Timeout"] (Arbitrary hash order)',
      delta: 'Inconsistent sorting on tie-break logs',
    },
  },
  {
    id: 'cache_default',
    name: 'Mutable Default Argument Implicit Caching',
    module: 'schedule_builder.py',
    description: "Removing Python's mutable default argument days=[] with days=None inadvertently wipes out an in-memory recurrence cache.",
    originalSnippet: 'def add_recurrence(event_id, rule, days=[]):\n    # Secretly relies on shared list across calls\n    days.append(rule)\n    return {"id": event_id, "cached_rules": list(days)}',
    naiveSnippet: 'def add_recurrence(event_id: str, rule: str, days: list | None = None) -> dict:\n    # Standard PEP linter "fix" wipes out accumulated rules!\n    if days is None:\n        days = []\n    days.append(rule)\n    return {"id": event_id, "cached_rules": days}',
    divergentCase: {
      input: 'Consecutive calls across 5 calendar events',
      expected: 'cached_rules accumulates 5 recurrence patterns',
      actual: 'cached_rules contains only 1 pattern per call',
      delta: 'Wipes accumulated recurrence cache',
    },
  },
];

export default function TrapPlaygroundModal({ isOpen, onClose }: TrapPlaygroundModalProps) {
  const [selectedId, setSelectedId] = useState<string>('rounding');
  const [probing, setProbing] = useState<boolean>(false);
  const [probeComplete, setProbeComplete] = useState<boolean>(false);

  if (!isOpen) return null;

  const current: TrapScenario = (SCENARIOS.find(s => s.id === selectedId) || SCENARIOS[0])!;

  const handleRunProbing = () => {
    setProbing(true);
    setProbeComplete(false);
    setTimeout(() => {
      setProbing(false);
      setProbeComplete(true);
    }, 600);
  };

  return (
    <div className="playground-backdrop" onClick={onClose}>
      <div className="playground-card" onClick={e => e.stopPropagation()}>
        <header className="playground-header">
          <div>
            <span className="playground-tag">Interactive Sandbox</span>
            <h3>Trap Playground: Can You Trick Plumbline?</h3>
          </div>
          <button className="close-btn" onClick={onClose} aria-label="Close modal">
            ✕
          </button>
        </header>

        <div className="playground-body">
          <div className="scenario-selector">
            {SCENARIOS.map(s => (
              <button
                key={s.id}
                className={`scenario-btn ${selectedId === s.id ? 'active' : ''}`}
                onClick={() => {
                  setSelectedId(s.id);
                  setProbeComplete(false);
                }}
              >
                {s.name}
              </button>
            ))}
          </div>

          <p className="scenario-desc">{current.description}</p>

          <div className="code-comparison-grid">
            <div className="code-panel">
              <span className="code-panel-label original">Original Legacy Code ({current.module})</span>
              <pre className="code-box">{current.originalSnippet}</pre>
            </div>
            <div className="code-panel">
              <span className="code-panel-label naive">Standard LLM "Clean" Refactor</span>
              <pre className="code-box">{current.naiveSnippet}</pre>
            </div>
          </div>

          <div className="action-center">
            <button
              className="run-probe-btn"
              onClick={handleRunProbing}
              disabled={probing}
            >
              {probing ? 'Running 50 Differential Probes in Sandboxes...' : '⚡ Probe for Behavioral Drift'}
            </button>
          </div>

          {probeComplete && (
            <div className="probe-result-banner">
              <div className="probe-result-header">
                <span className="result-alert-icon">⚠️</span>
                <strong>BEHAVIORAL DRIFT DETECTED: 7 / 50 Probes Diverged!</strong>
              </div>
              <p className="result-explanation">
                Standard model unit tests marked this candidate <strong>100% GREEN</strong>. Plumbline’s differential probe discovered the exact invariant failure:
              </p>
              <div className="divergence-table-wrap">
                <table className="divergence-table">
                  <thead>
                    <tr>
                      <th>Test Input</th>
                      <th>Original Invariant</th>
                      <th>Candidate Result</th>
                      <th>Divergence Impact</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td><code>{current.divergentCase.input}</code></td>
                      <td className="text-original">{current.divergentCase.expected}</td>
                      <td className="text-divergent">{current.divergentCase.actual}</td>
                      <td className="text-danger">{current.divergentCase.delta}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div className="verdict-tag">
                Plumbline Verdict: <strong>DROPPED (DOES NOT HOLD)</strong>
              </div>
            </div>
          )}
        </div>

        <footer className="playground-footer">
          <span>Probes run side-by-side in dual Token Factory Copy-on-Write Sandbox forks.</span>
          <button className="done-btn" onClick={onClose}>Close Playground</button>
        </footer>
      </div>
    </div>
  );
}
