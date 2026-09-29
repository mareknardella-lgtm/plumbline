import { useState, useEffect } from 'react'

interface HealthStatus {
  status: string
  replay_only: boolean
}

export function App() {
  const [health, setHealth] = useState<HealthStatus | null>(null)

  useEffect(() => {
    fetch('/api/health')
      .then(r => r.json())
      .then(setHealth)
      .catch(() => setHealth(null))
  }, [])

  return (
    <div className="app">
      <header className="header">
        <div className="header__mark">
          <svg width="24" height="32" viewBox="0 0 24 32" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
            <path d="M12 2 C10 2 10 4 12 4 L12 4" stroke="currentColor" strokeWidth="1.5" fill="none" />
            <line x1="12" y1="4" x2="12" y2="26" stroke="currentColor" strokeWidth="1.5" />
            <path d="M12 26 L8 30 L12 32 L16 30 Z" fill="currentColor" />
          </svg>
          <span className="header__wordmark">Plumbline</span>
        </div>
        <div className="header__status">
          {health ? (
            <span className={`status-dot status-dot--${health.status === 'ok' ? 'live' : 'replay'}`} />
          ) : null}
          <span>{health?.replay_only ? 'Replay only' : health ? 'Live' : 'Connecting…'}</span>
        </div>
      </header>

      <main className="main">
        <section className="hero">
          <h1>Refactor old code without changing what it does.</h1>
          <p>
            Plumbline records how your code behaves today, plants bugs in it to
            check that record, then tests every refactor against it and shows the evidence.
          </p>
        </section>

        <section className="start-panel">
          <p className="start-panel__placeholder">
            Start panel will be built in Phase 3.
          </p>
        </section>
      </main>

      <footer className="footer">
        <p>Built with NVIDIA Nemotron on Nebius Token Factory. Open source under MIT.</p>
      </footer>
    </div>
  )
}
