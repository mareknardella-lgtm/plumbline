import React, { useState } from 'react';
import './HomeScreen.css';
import Button from '../components/Button';
import Chip from '../components/Chip';
import SegmentedControl from '../components/SegmentedControl';
import { createRun } from '../lib/api';

export default function HomeScreen() {
  const [tab, setTab] = useState('sample');
  const [depth, setDepth] = useState('quick');
  const [goal, setGoal] = useState('test');

  const handleStartRun = async () => {
    try {
      const res = await createRun({ type: tab, depth, goal });
      window.location.hash = `#/run/${res.id}`;
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="home-screen">
      <header className="home-header">
        <div className="logo">Plumbline</div>
        <nav>
          <a href="#how-it-works">How it works</a>
        </nav>
      </header>
      
      <main className="home-main">
        <section className="hero-section">
          <h1>Prove your code works.</h1>
          <p>Plumbline runs comprehensive testing strategies and produces a verifiable dossier of evidence.</p>
        </section>

        <section className="start-panel">
          <div className="tabs">
            {['sample', 'paste', 'upload'].map(t => (
              <button 
                key={t}
                className={`tab ${tab === t ? 'active' : ''}`}
                onClick={() => setTab(t)}
              >
                {t === 'sample' ? 'Sample project' : t === 'paste' ? 'Paste code' : 'Upload zip'}
              </button>
            ))}
          </div>

          <div className="start-controls">
            <div className="control-group">
              <label>Goal</label>
              <div className="chips">
                <Chip label="Test" selected={goal === 'test'} onClick={() => setGoal('test')} />
                <Chip label="Refactor" selected={goal === 'refactor'} onClick={() => setGoal('refactor')} />
              </div>
            </div>

            <div className="control-group">
              <label>Depth</label>
              <SegmentedControl 
                options={[{ label: 'Quick', value: 'quick' }, { label: 'Thorough', value: 'thorough' }]}
                value={depth}
                onChange={setDepth}
              />
            </div>
            
            <Button variant="primary" size="md" onClick={handleStartRun} className="start-btn">
              Start run
            </Button>
          </div>
        </section>
      </main>
    </div>
  );
}
