import React, { useState, useEffect } from 'react';
import ErrorBoundary from './ErrorBoundary';
import NotFound from './NotFound';
import HomeScreen from '../screens/HomeScreen';
import CockpitScreen from '../screens/CockpitScreen';
import DossierScreen from '../screens/DossierScreen';
import './App.css';

export default function App() {
  const [route, setRoute] = useState(window.location.hash || '#/');
  const [theme, setTheme] = useState<'light' | 'dark'>('light');

  useEffect(() => {
    const handleHashChange = () => setRoute(window.location.hash || '#/');
    window.addEventListener('hashchange', handleHashChange);
    return () => window.removeEventListener('hashchange', handleHashChange);
  }, []);

  useEffect(() => {
    try {
      const savedTheme = localStorage.getItem('theme');
      if (savedTheme === 'dark' || savedTheme === 'light') {
        setTheme(savedTheme);
      }
    } catch (e) {
      // Ignore
    }
  }, []);

  const toggleTheme = () => {
    const newTheme = theme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
    document.documentElement.setAttribute('data-theme', newTheme);
    try {
      localStorage.setItem('theme', newTheme);
    } catch (e) {
      // Ignore
    }
  };

  let content;
  if (route === '#/') {
    content = <HomeScreen />;
  } else if (route.startsWith('#/run/')) {
    const id = route.split('/')[2];
    content = <CockpitScreen runId={id} />;
  } else if (route.startsWith('#/dossier/')) {
    const id = route.split('/')[2];
    content = <DossierScreen runId={id} />;
  } else {
    content = <NotFound />;
  }

  return (
    <ErrorBoundary>
      <div className={`app-container theme-${theme}`}>
        <a href="#main-content" className="skip-link">Skip to main content</a>
        <button onClick={toggleTheme} className="theme-toggle">
          Toggle Theme
        </button>
        <main id="main-content">
          {content}
        </main>
      </div>
    </ErrorBoundary>
  );
}
