import { useState } from 'react';
import './HomeScreen.css';
import Button from '../components/Button';
import Chip from '../components/Chip';
import SegmentedControl from '../components/SegmentedControl';
import { createRun } from '../lib/api';

export default function HomeScreen() {
  const [tab, setTab] = useState('sample');
  const [specimen, setSpecimen] = useState('invoice_totals');
  const [depth, setDepth] = useState('quick');
  const [goal, setGoal] = useState('Modernize to Python 3.12');
  const [pasteCode, setPasteCode] = useState('');
  const [loading, setLoading] = useState(false);

  const handleStartRun = async () => {
    setLoading(true);
    try {
      const res = await createRun({
        source: tab === 'sample' ? 'specimen' : tab,
        specimen_name: specimen,
        mode: depth,
        goal,
        code: tab === 'paste' ? pasteCode : '',
      });
      if (res && res.id) {
        window.location.hash = `#/run/${res.id}`;
      }
    } catch (e) {
      console.error('Failed to create run:', e);
    } finally {
      setLoading(false);
    }
  };

  const specimens = [
    {
      id: 'invoice_totals',
      title: 'invoice_totals.py',
      lines: 232,
      hint: 'Rounds prices two ways (banker’s vs half-up)',
    },
    {
      id: 'log_digester',
      title: 'log_digester.py',
      lines: 200,
      hint: 'Depends on dictionary insertion order and sort ties',
    },
    {
      id: 'schedule_builder',
      title: 'schedule_builder.py',
      lines: 244,
      hint: 'Deprecated utcnow() and mutable default recurrence trap',
    },
  ];

  const goals = [
    'Modernize to Python 3.12',
    'Reduce complexity',
    'Add type hints',
    'Preserve exact behavior',
  ];

  return (
    <div className="home-screen">
      <header className="home-header">
        <div className="logo-container">
          <span className="logo-mark">⌖</span>
          <span className="logo-text">Plumbline</span>
        </div>
        <div className="header-status">
          <span className="status-dot online" />
          <span className="status-label">Live • Token Factory Sandboxes</span>
        </div>
      </header>

      <main className="home-main">
        <section className="hero-section">
          <h1>Refactor old code without changing what it does.</h1>
          <p className="hero-sub">
            Plumbline pins behavior with isolated tests, plants AST bugs to prove test strength,
            and runs differential probes before declaring a refactor true.
          </p>
        </section>

        <section className="start-panel">
          <div className="tabs">
            <button
              className={`tab ${tab === 'sample' ? 'active' : ''}`}
              onClick={() => setTab('sample')}
            >
              Sample project
            </button>
            <button
              className={`tab ${tab === 'paste' ? 'active' : ''}`}
              onClick={() => setTab('paste')}
            >
              Paste code
            </button>
          </div>

          <div className="start-controls">
            {tab === 'sample' ? (
              <div className="control-group">
                <label className="group-label">Choose legacy specimen</label>
                <div className="specimen-grid">
                  {specimens.map(s => (
                    <div
                      key={s.id}
                      className={`specimen-card ${specimen === s.id ? 'selected' : ''}`}
                      onClick={() => setSpecimen(s.id)}
                    >
                      <div className="specimen-title">{s.title}</div>
                      <div className="specimen-lines">{s.lines} lines</div>
                      <div className="specimen-hint">{s.hint}</div>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <div className="control-group">
                <label className="group-label">Paste Python source</label>
                <textarea
                  className="paste-input"
                  rows={8}
                  placeholder="Paste Python module code here..."
                  value={pasteCode}
                  onChange={e => setPasteCode(e.target.value)}
                />
              </div>
            )}

            <div className="control-group">
              <label className="group-label">Goal</label>
              <div className="chips">
                {goals.map(g => (
                  <Chip
                    key={g}
                    label={g}
                    selected={goal === g}
                    onClick={() => setGoal(g)}
                  />
                ))}
              </div>
            </div>

            <div className="control-group">
              <label className="group-label">Verification depth</label>
              <SegmentedControl
                options={[
                  { label: 'Quick (2 candidates, ~30s)', value: 'quick' },
                  { label: 'Thorough (3 candidates, ~1m)', value: 'thorough' },
                ]}
                value={depth}
                onChange={setDepth}
              />
            </div>

            <div className="action-row">
              <Button
                variant="primary"
                size="md"
                onClick={handleStartRun}
                disabled={loading || (tab === 'paste' && !pasteCode.trim())}
              >
                {loading ? 'Starting run...' : 'Start run'}
              </Button>
              <span className="sandbox-notice">
                Code runs only in isolated Token Factory Sandboxes.
              </span>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}
