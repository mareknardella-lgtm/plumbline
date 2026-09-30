import { useState, useEffect } from 'react';
import './Navbar.css';
import { isSoundEnabled, setSoundEnabled, playTick } from '../lib/sound';

interface NavbarProps {
  onOpenArch?: () => void;
  onOpenBench?: () => void;
  onOpenAiStudy?: () => void;
  onOpenTrapPlayground?: () => void;
  theme?: 'light' | 'dark';
  onToggleTheme?: () => void;
}

export default function Navbar({
  onOpenArch,
  onOpenBench,
  onOpenAiStudy,
  onOpenTrapPlayground,
  theme,
  onToggleTheme,
}: NavbarProps) {
  const [sound, setSound] = useState(isSoundEnabled());

  useEffect(() => {
    setSound(isSoundEnabled());
  }, []);

  const handleToggleSound = () => {
    const next = !sound;
    setSound(next);
    setSoundEnabled(next);
    if (next) playTick();
  };

  return (
    <header className="navbar">
      <div className="navbar__brand" onClick={() => (window.location.hash = '#/')}>
        <div className="navbar__logo-bob">
          <span className="navbar__plumb-symbol">⌖</span>
        </div>
        <div className="navbar__titles">
          <div className="navbar__name">Plumbline</div>
          <div className="navbar__tagline">Autonomous Behavior Verification</div>
        </div>
        <span className="navbar__hackathon-pill">
          <span className="hackathon-gradient-dot" />
          Nebius × NVIDIA
        </span>
      </div>

      <nav className="navbar__actions" aria-label="Main navigation">
        {onOpenArch && (
          <button
            type="button"
            className="navbar__nav-btn"
            onClick={onOpenArch}
            title="Inspect 6-stage architecture and COW fork tree"
          >
            <span className="nav-btn__icon">📐</span>
            <span>Architecture</span>
          </button>
        )}

        {onOpenBench && (
          <button
            type="button"
            className="navbar__nav-btn"
            onClick={onOpenBench}
            title="View empirical sandbox fork benchmarks (11.2x speedup)"
          >
            <span className="nav-btn__icon">⚡</span>
            <span>Benchmarks <span className="nav-btn__badge">11.2x</span></span>
          </button>
        )}

        {onOpenAiStudy && (
          <button
            type="button"
            className="navbar__nav-btn"
            onClick={onOpenAiStudy}
            title="Review empirical study: standard AI drift vs Plumbline"
          >
            <span className="nav-btn__icon">📊</span>
            <span>AI Study <span className="nav-btn__badge drift">78% Drift</span></span>
          </button>
        )}

        {onOpenTrapPlayground && (
          <button
            type="button"
            className="navbar__nav-btn highlight"
            onClick={onOpenTrapPlayground}
            title="Interactive challenge: stress-test legacy traps against 50 differential probes"
          >
            <span className="nav-btn__icon">🎮</span>
            <span>Trap Playground</span>
          </button>
        )}

        <a
          href="https://github.com/mareknardella-lgtm/plumbline"
          target="_blank"
          rel="noopener noreferrer"
          className="navbar__nav-btn github"
          title="Open official GitHub repository"
        >
          <svg className="github-icon" viewBox="0 0 16 16" width="14" height="14" fill="currentColor">
            <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z" />
          </svg>
          <span>v1.3.0</span>
        </a>

        <div className="navbar__divider" />

        {/* Audio feedback button */}
        <button
          type="button"
          className={`navbar__sound-btn ${sound ? 'active' : 'muted'}`}
          onClick={handleToggleSound}
          title={sound ? 'Procedural Web Audio FX enabled' : 'Sound muted'}
          aria-label={sound ? 'Mute procedural sound' : 'Enable procedural sound'}
        >
          {sound ? '🔊' : '🔇'}
        </button>

        {/* Theme toggle if provided */}
        {onToggleTheme && (
          <button
            type="button"
            className="navbar__theme-btn"
            onClick={onToggleTheme}
            title={`Switch to ${theme === 'light' ? 'dark' : 'light'} theme`}
            aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} theme`}
          >
            {theme === 'light' ? '🌙' : '☀️'}
          </button>
        )}

        <div className="navbar__status-pill" title="Connected to Token Factory Sandboxes daemon">
          <span className="pulse-dot" />
          <span className="status-text">Sandboxes Live</span>
        </div>
      </nav>
    </header>
  );
}
