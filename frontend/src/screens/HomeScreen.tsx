import { useState } from 'react';
import './HomeScreen.css';
import Button from '../components/Button';
import Chip from '../components/Chip';
import SegmentedControl from '../components/SegmentedControl';
import ArchitectureDrawer from '../components/ArchitectureDrawer';
import BenchmarksModal from '../components/BenchmarksModal';
import AIVsPlumblineModal from '../components/AIVsPlumblineModal';
import TrapPlaygroundModal from '../components/TrapPlaygroundModal';
import { createRun } from '../lib/api';

export default function HomeScreen() {
  const [tab, setTab] = useState('sample');
  const [specimen, setSpecimen] = useState('invoice_totals');
  const [depth, setDepth] = useState('quick');
  const [goal, setGoal] = useState('Modernize to Python 3.12');
  const [pasteCode, setPasteCode] = useState('');
  const [loading, setLoading] = useState(false);
  const [isArchOpen, setIsArchOpen] = useState(false);
  const [isBenchOpen, setIsBenchOpen] = useState(false);
  const [isAiStudyOpen, setIsAiStudyOpen] = useState(false);
  const [isTrapPlaygroundOpen, setIsTrapPlaygroundOpen] = useState(false);
  const [githubUrl, setGithubUrl] = useState('');
  const [fetchingUrl, setFetchingUrl] = useState(false);
  const [apiKey, setApiKey] = useState(() => sessionStorage.getItem('nebius_byok_key') || '');
  const [showApiKeyInput, setShowApiKeyInput] = useState(false);

  const handleFetchGithub = async () => {
    if (!githubUrl.trim()) return;
    setFetchingUrl(true);
    try {
      let url = githubUrl.trim();
      if (url.includes('github.com') && url.includes('/blob/')) {
        url = url.replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/');
      }
      const res = await fetch(url);
      if (res.ok) {
        const text = await res.text();
        setPasteCode(text);
      } else {
        alert('Failed to fetch from URL: ' + res.statusText);
      }
    } catch {
      alert('Error fetching from URL. Ensure the repository is public.');
    } finally {
      setFetchingUrl(false);
    }
  };

  const handleStartRun = async () => {
    setLoading(true);
    try {
      const res = await createRun({
        source: tab === 'sample' ? 'specimen' : tab,
        specimen_name: specimen,
        mode: depth,
        goal,
        code: tab === 'paste' ? pasteCode : '',
        api_key: apiKey.trim() || undefined,
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
    {
      id: 'currency_exchange',
      title: 'currency_exchange.ts (P2 Multi-Lang)',
      lines: 160,
      hint: 'IEEE-754 precision & JS Math.round negative integer trap',
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
        <div className="header-actions">
          <button
            type="button"
            className="how-it-works-btn"
            onClick={() => setIsArchOpen(true)}
            aria-label="Open architecture and system design drawer"
          >
            How it works
          </button>
          <button
            type="button"
            className="how-it-works-btn"
            onClick={() => setIsBenchOpen(true)}
            aria-label="Open empirical benchmarks and evaluation report"
          >
            Benchmarks
          </button>
          <button
            type="button"
            className="how-it-works-btn"
            onClick={() => setIsAiStudyOpen(true)}
            aria-label="Open Standard AI vs Plumbline comparative study"
          >
            AI vs Plumbline Study
          </button>
          <button
            type="button"
            className="how-it-works-btn"
            onClick={() => setIsTrapPlaygroundOpen(true)}
            aria-label="Open interactive Trap Playground"
          >
            Trap Playground
          </button>
          <div className="header-status">
            <span className="status-dot online" />
            <span className="status-label">Live • Token Factory Sandboxes</span>
          </div>
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
            <button
              className={`tab ${tab === 'upload' ? 'active' : ''}`}
              onClick={() => setTab('upload')}
            >
              Upload zip
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
            ) : tab === 'paste' ? (
              <div className="control-group">
                <div className="group-label-row">
                  <label className="group-label">Paste Python source</label>
                  <span className="group-hint">or import from a public GitHub URL</span>
                </div>
                <div className="url-import-row">
                  <input
                    type="url"
                    placeholder="https://github.com/user/repo/blob/main/module.py"
                    className="url-import-input"
                    value={githubUrl}
                    onChange={(e) => setGithubUrl(e.target.value)}
                  />
                  <Button
                    variant="secondary"
                    size="sm"
                    onClick={handleFetchGithub}
                    disabled={!githubUrl.trim() || fetchingUrl}
                  >
                    {fetchingUrl ? 'Fetching...' : 'Import URL'}
                  </Button>
                </div>
                <textarea
                  className="paste-input"
                  rows={8}
                  placeholder="Paste Python module code here..."
                  value={pasteCode}
                  onChange={(e) => setPasteCode(e.target.value)}
                />
              </div>
            ) : (
              <div className="control-group">
                <label className="group-label">Upload Python module or archive</label>
                <div className="upload-box">
                  <input
                    type="file"
                    id="file-upload"
                    accept=".py,.zip"
                    className="file-input-hidden"
                    onChange={async (e) => {
                      const file = e.target.files?.[0];
                      if (file) {
                        const text = await file.text();
                        setPasteCode(text);
                      }
                    }}
                  />
                  <label htmlFor="file-upload" className="upload-label">
                    <span className="upload-icon">📁</span>
                    <span className="upload-prompt">Click to select <code>.py</code> or <code>.zip</code></span>
                    <span className="upload-hint">Files are processed in isolated Token Factory Sandboxes</span>
                  </label>
                  {pasteCode && (
                    <div className="file-loaded-banner">
                      ✓ Code loaded ({pasteCode.split('\n').length} lines)
                    </div>
                  )}
                </div>
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

            <div className="byok-section">
              <button
                type="button"
                className="byok-toggle-btn"
                onClick={() => setShowApiKeyInput(!showApiKeyInput)}
              >
                🔑 {showApiKeyInput ? 'Hide Custom API Key' : 'Bring Your Own Key (Optional BYOK)'}
              </button>
              {showApiKeyInput && (
                <div className="byok-input-container">
                  <input
                    type="password"
                    placeholder="Enter Nebius Token Factory Key (sk-...)"
                    value={apiKey}
                    onChange={(e) => {
                      setApiKey(e.target.value);
                      sessionStorage.setItem('nebius_byok_key', e.target.value);
                    }}
                    className="byok-input"
                  />
                  <span className="byok-hint">
                    Bypasses demo rate limits. Kept only in this browser session.
                  </span>
                </div>
              )}
            </div>

            <div className="action-row">
              <Button
                variant="primary"
                size="md"
                onClick={handleStartRun}
                disabled={loading || ((tab === 'paste' || tab === 'upload') && !pasteCode.trim())}
              >
                {loading ? 'Starting run...' : 'Start run'}
              </Button>
              <Button
                variant="secondary"
                size="md"
                onClick={() => {
                  window.location.hash = '#/run/2407642b-b5aa-4bfe-844d-81301c86beaf';
                }}
              >
                Watch a recorded run
              </Button>
              <span className="sandbox-notice">
                Code runs only in isolated Token Factory Sandboxes.
              </span>
            </div>
          </div>
        </section>
      </main>

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
