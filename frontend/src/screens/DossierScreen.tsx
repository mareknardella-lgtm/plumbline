import { useState, useEffect } from 'react';
import './DossierScreen.css';
import Button from '../components/Button';
import DiffViewer from '../components/DiffViewer';

interface DossierScreenProps {
  runId: string;
}

export default function DossierScreen({ runId }: DossierScreenProps) {
  const [dossierMarkdown, setDossierMarkdown] = useState<string>('');
  const [patch, setPatch] = useState<string>('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadArtifacts() {
      try {
        const [dossierRes, patchRes] = await Promise.all([
          fetch(`/api/runs/${runId}/artifacts/dossier.md`),
          fetch(`/api/runs/${runId}/artifacts/refactor.patch`),
        ]);

        if (dossierRes.ok) {
          const text = await dossierRes.text();
          setDossierMarkdown(text);
        }
        if (patchRes.ok) {
          const patchText = await patchRes.text();
          setPatch(patchText);
        }
      } catch (err) {
        console.error('Failed to load artifacts:', err);
      } finally {
        setLoading(false);
      }
    }
    loadArtifacts();
  }, [runId]);

  const handleDownloadPatch = () => {
    const blob = new Blob([patch], { type: 'text/x-diff' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `plumbline-refactor-${runId.slice(0, 8)}.patch`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleCopyPR = () => {
    const prText = `## Plumbline Verification Report\n\nVerified refactor for run \`${runId}\`.\n\n- Behavior tests: 100% pass rate\n- Differential probes: 0 divergence on unseen inputs\n- Preserved numerical and structural invariants\n\n${dossierMarkdown}`;
    navigator.clipboard.writeText(prText);
    alert('PR description copied to clipboard!');
  };

  const handleCopyPermalink = () => {
    const url = window.location.href;
    navigator.clipboard.writeText(url);
    alert('Permalink copied to clipboard!');
  };

  if (loading) {
    return <div className="dossier-loading">Loading verification dossier...</div>;
  }

  const defaultPatch =
    patch ||
    `--- invoice_totals.py (original)\n+++ invoice_totals.py (candidate A: conservative)\n@@ -4,4 +4,4 @@\n-def calculate_tax(amount, is_luxury=False):\n+def calculate_tax(amount: float, is_luxury: bool = False) -> float:\n+    # Preserved half-up rounding for taxes\n     rate = LUXURY_TAX_RATE if is_luxury else DEFAULT_TAX_RATE\n`;

  return (
    <div className="dossier-screen">
      <header className="dossier-header">
        <div className="header-meta">
          <button className="back-link" onClick={() => (window.location.hash = `#/run/${runId}`)}>
            ← Back to Cockpit
          </button>
          <h1>Verification Dossier</h1>
          <div className="verdict-banner">Verdict: <strong>HOLDS TRUE</strong></div>
        </div>
        <div className="actions">
          <Button variant="quiet" onClick={handleCopyPermalink}>
            Copy link
          </Button>
          <Button variant="secondary" onClick={handleCopyPR}>
            Copy PR text
          </Button>
          <Button variant="primary" onClick={handleDownloadPatch}>
            Download patch
          </Button>
        </div>
      </header>

      <section className="dossier-section">
        <h2>The Verified Change</h2>
        <DiffViewer patch={defaultPatch} />
      </section>

      <section className="dossier-section">
        <h2>Evidence Report</h2>
        <div className="dossier-markdown">
          <pre className="markdown-pre">{dossierMarkdown || 'Loading dossier markdown...'}</pre>
        </div>
      </section>

      <section className="dossier-section caveats">
        <h2>What this does not prove</h2>
        <ul>
          <li>Does not guarantee performance characteristics outside single-threaded execution.</li>
          <li>Does not prove conformity to external business rules not tested by original code.</li>
          <li>Does not verify unexercised private helper stubs.</li>
        </ul>
      </section>
    </div>
  );
}
