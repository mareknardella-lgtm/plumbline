import React from 'react';
import './DossierScreen.css';
import Button from '../components/Button';
import DiffViewer from '../components/DiffViewer';

interface DossierScreenProps {
  runId: string;
}

export default function DossierScreen({ runId }: DossierScreenProps) {
  // Normally fetch dossier from backend here. Mocking for now.
  const mockPatch = `--- a/src/index.js\n+++ b/src/index.js\n@@ -1,3 +1,3 @@\n-const a = 1;\n+const a = 2;\n console.log(a);`;

  return (
    <div className="dossier-screen">
      <header className="dossier-header">
        <h1>Dossier for Run: {runId}</h1>
        <div className="actions">
          <Button variant="secondary">Copy PR text</Button>
          <Button variant="primary">Download patch</Button>
        </div>
      </header>
      
      <section className="dossier-section">
        <h2>The Change</h2>
        <DiffViewer patch={mockPatch} />
      </section>

      <section className="dossier-section">
        <h2>How we checked</h2>
        <p>This code was checked with 10 mutants and comprehensive tests.</p>
      </section>
    </div>
  );
}
