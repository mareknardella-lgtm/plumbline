import React, { useEffect } from 'react';
import './ArchitectureDrawer.css';
import Button from './Button';

interface ArchitectureDrawerProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function ArchitectureDrawer({ isOpen, onClose }: ArchitectureDrawerProps) {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div className="drawer-overlay" onClick={onClose} role="presentation">
      <div
        className="drawer-panel"
        role="dialog"
        aria-modal="true"
        aria-labelledby="drawer-title"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="drawer-header">
          <div className="drawer-title-group">
            <span className="drawer-badge">System Design</span>
            <h2 id="drawer-title">How Plumbline Works</h2>
          </div>
          <Button variant="quiet" size="sm" onClick={onClose} aria-label="Close drawer">
            ✕ Close
          </Button>
        </div>

        <div className="drawer-body">
          <p className="drawer-lead">
            Plumbline combines NVIDIA Nemotron 3 model tiers with isolated Token Factory Sandboxes
            to verify that refactored code preserves identical runtime behavior.
          </p>

          <div className="architecture-diagram-container" id="architecture-diagram">
            <h3 className="section-label">Architecture & Fork Hierarchy</h3>
            <svg
              className="arch-svg"
              viewBox="0 0 880 540"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
              aria-label="Plumbline system architecture and sandbox fork hierarchy diagram"
            >
              {/* Background */}
              <rect width="880" height="540" rx="8" fill="var(--bg-subtle, #f8fafc)" stroke="var(--border, #e2e8f0)" />

              {/* Orchestrator Top Box */}
              <rect x="240" y="24" width="400" height="60" rx="6" fill="var(--bg, #ffffff)" stroke="var(--border, #cbd5e1)" strokeWidth="1.5" />
              <text x="440" y="48" textAnchor="middle" fill="var(--text, #0f172a)" fontWeight="600" fontSize="14" fontFamily="var(--font-ui, sans-serif)">Plumbline Orchestrator</text>
              <text x="440" y="68" textAnchor="middle" fill="var(--text-muted, #64748b)" fontSize="11" fontFamily="var(--font-code, monospace)">FastAPI • Event Bus • Token Factory AsyncOpenAI</text>

              {/* Connecting Line from Orchestrator */}
              <path d="M440 84 V120" stroke="var(--border, #cbd5e1)" strokeWidth="2" strokeDasharray="4 4" />

              {/* Model Tiers Column (Left) */}
              <rect x="40" y="120" width="240" height="200" rx="6" fill="var(--bg, #ffffff)" stroke="var(--border, #cbd5e1)" strokeWidth="1.5" />
              <rect x="40" y="120" width="240" height="32" rx="6" fill="var(--accent-dim, #f1f5f9)" />
              <text x="160" y="141" textAnchor="middle" fill="var(--text, #0f172a)" fontWeight="600" fontSize="12" fontFamily="var(--font-ui, sans-serif)">NVIDIA Nemotron Models</text>
              
              <text x="56" y="176" fill="var(--plumb, #10b981)" fontWeight="600" fontSize="11" fontFamily="var(--font-code, monospace)">• Ultra 550b</text>
              <text x="56" y="192" fill="var(--text-muted, #64748b)" fontSize="10" fontFamily="var(--font-ui, sans-serif)">Survey analysis & Ambitious refactor</text>
              
              <text x="56" y="220" fill="var(--plumb, #10b981)" fontWeight="600" fontSize="11" fontFamily="var(--font-code, monospace)">• Super 120b</text>
              <text x="56" y="236" fill="var(--text-muted, #64748b)" fontSize="10" fontFamily="var(--font-ui, sans-serif)">Pytest pins, Balanced refactor, Dossier</text>
              
              <text x="56" y="264" fill="var(--plumb, #10b981)" fontWeight="600" fontSize="11" fontFamily="var(--font-code, monospace)">• Nano 30b</text>
              <text x="56" y="280" fill="var(--text-muted, #64748b)" fontSize="10" fontFamily="var(--font-ui, sans-serif)">Survivor triage & Differential probes</text>
              
              <text x="56" y="304" fill="var(--text-muted, #64748b)" fontSize="10" fontFamily="var(--font-code, monospace)">• Lightning 3.5: Fast fallback</text>

              {/* Token Factory Sandboxes Fork Tree (Center & Right) */}
              <rect x="320" y="120" width="520" height="200" rx="6" fill="var(--bg, #ffffff)" stroke="var(--border, #cbd5e1)" strokeWidth="1.5" />
              <rect x="320" y="120" width="520" height="32" rx="6" fill="var(--accent-dim, #f1f5f9)" />
              <text x="580" y="141" textAnchor="middle" fill="var(--text, #0f172a)" fontWeight="600" fontSize="12" fontFamily="var(--font-ui, sans-serif)">Token Factory Sandboxes (Copy-on-Write)</text>

              {/* Baseline Node */}
              <rect x="470" y="165" width="220" height="36" rx="4" fill="var(--bg-subtle, #f8fafc)" stroke="var(--plumb, #10b981)" strokeWidth="1.5" />
              <circle cx="484" cy="183" r="4" fill="var(--plumb, #10b981)" />
              <text x="496" y="186" fill="var(--text, #0f172a)" fontWeight="600" fontSize="11" fontFamily="var(--font-code, monospace)">Baseline Checkpoint</text>

              {/* Branch lines */}
              <path d="M580 201 V225" stroke="var(--border, #cbd5e1)" strokeWidth="1.5" />
              <path d="M370 225 H790" stroke="var(--border, #cbd5e1)" strokeWidth="1.5" />
              <path d="M370 225 V245" stroke="var(--border, #cbd5e1)" strokeWidth="1.5" />
              <path d="M510 225 V245" stroke="var(--border, #cbd5e1)" strokeWidth="1.5" />
              <path d="M650 225 V245" stroke="var(--border, #cbd5e1)" strokeWidth="1.5" />
              <path d="M790 225 V245" stroke="var(--border, #cbd5e1)" strokeWidth="1.5" />

              {/* Mutants Fork */}
              <rect x="330" y="245" width="120" height="52" rx="4" fill="var(--bg, #ffffff)" stroke="var(--border, #cbd5e1)" />
              <text x="390" y="264" textAnchor="middle" fill="var(--text, #0f172a)" fontWeight="600" fontSize="10">Mutant Forks</text>
              <text x="390" y="278" textAnchor="middle" fill="var(--text-muted, #64748b)" fontSize="9">30 parallel forks</text>
              <text x="390" y="290" textAnchor="middle" fill="var(--plumb, #10b981)" fontSize="9" fontWeight="600">1.64ms setup</text>

              {/* Candidate A Fork */}
              <rect x="465" y="245" width="110" height="52" rx="4" fill="var(--bg, #ffffff)" stroke="var(--border, #cbd5e1)" />
              <text x="520" y="264" textAnchor="middle" fill="var(--text, #0f172a)" fontWeight="600" fontSize="10">Candidate A</text>
              <text x="520" y="278" textAnchor="middle" fill="var(--text-muted, #64748b)" fontSize="9">Conservative</text>
              <text x="520" y="290" textAnchor="middle" fill="var(--text-muted, #64748b)" fontSize="9">Hash-locked</text>

              {/* Candidate B Fork */}
              <rect x="605" y="245" width="110" height="52" rx="4" fill="var(--bg, #ffffff)" stroke="var(--border, #cbd5e1)" />
              <text x="660" y="264" textAnchor="middle" fill="var(--text, #0f172a)" fontWeight="600" fontSize="10">Candidate B</text>
              <text x="660" y="278" textAnchor="middle" fill="var(--text-muted, #64748b)" fontSize="9">Balanced</text>
              <text x="660" y="290" textAnchor="middle" fill="var(--text-muted, #64748b)" fontSize="9">Hash-locked</text>

              {/* Differential Probes */}
              <rect x="735" y="245" width="110" height="52" rx="4" fill="var(--bg, #ffffff)" stroke="var(--border, #cbd5e1)" />
              <text x="790" y="264" textAnchor="middle" fill="var(--text, #0f172a)" fontWeight="600" fontSize="10">Probes Fork</text>
              <text x="790" y="278" textAnchor="middle" fill="var(--text-muted, #64748b)" fontSize="9">50 unseen inputs</text>
              <text x="790" y="290" textAnchor="middle" fill="var(--text-muted, #64748b)" fontSize="9">Side-by-side</text>

              {/* Six Stages Bottom Strip */}
              <rect x="40" y="345" width="800" height="165" rx="6" fill="var(--bg, #ffffff)" stroke="var(--border, #cbd5e1)" strokeWidth="1.5" />
              <text x="60" y="372" fill="var(--text, #0f172a)" fontWeight="600" fontSize="13" fontFamily="var(--font-ui, sans-serif)">Verification Pipeline Flow</text>

              {/* Stage Boxes */}
              {/* Stage 1 */}
              <g transform="translate(60, 390)">
                <rect width="115" height="95" rx="4" fill="var(--bg-subtle, #f8fafc)" stroke="var(--border, #e2e8f0)" />
                <text x="12" y="22" fill="var(--plumb, #10b981)" fontWeight="700" fontSize="11">1. Survey</text>
                <text x="12" y="42" fill="var(--text, #0f172a)" fontSize="10" fontWeight="500">AST pre-pass</text>
                <text x="12" y="58" fill="var(--text-muted, #64748b)" fontSize="9">Flag effects</text>
                <text x="12" y="74" fill="var(--text-muted, #64748b)" fontSize="9">Nemotron Ultra</text>
              </g>

              {/* Arrow */}
              <path d="M182 437 H194" stroke="var(--text-muted, #94a3b8)" strokeWidth="1.5" markerEnd="url(#arrow)" />

              {/* Stage 2 */}
              <g transform="translate(196, 390)">
                <rect width="115" height="95" rx="4" fill="var(--bg-subtle, #f8fafc)" stroke="var(--border, #e2e8f0)" />
                <text x="12" y="22" fill="var(--plumb, #10b981)" fontWeight="700" fontSize="11">2. Record</text>
                <text x="12" y="42" fill="var(--text, #0f172a)" fontSize="10" fontWeight="500">Pytest pins</text>
                <text x="12" y="58" fill="var(--text-muted, #64748b)" fontSize="9">Hermetic harness</text>
                <text x="12" y="74" fill="var(--text-muted, #64748b)" fontSize="9">Nemotron Super</text>
              </g>

              {/* Arrow */}
              <path d="M318 437 H330" stroke="var(--text-muted, #94a3b8)" strokeWidth="1.5" />

              {/* Stage 3 */}
              <g transform="translate(332, 390)">
                <rect width="115" height="95" rx="4" fill="var(--bg-subtle, #f8fafc)" stroke="var(--border, #e2e8f0)" />
                <text x="12" y="22" fill="var(--plumb, #10b981)" fontWeight="700" fontSize="11">3. Mutate</text>
                <text x="12" y="42" fill="var(--text, #0f172a)" fontSize="10" fontWeight="500">AST tripwires</text>
                <text x="12" y="58" fill="var(--text-muted, #64748b)" fontSize="9">30 COW forks</text>
                <text x="12" y="74" fill="var(--text-muted, #64748b)" fontSize="9">Strength ≥ 85%</text>
              </g>

              {/* Arrow */}
              <path d="M454 437 H466" stroke="var(--text-muted, #94a3b8)" strokeWidth="1.5" />

              {/* Stage 4 */}
              <g transform="translate(468, 390)">
                <rect width="115" height="95" rx="4" fill="var(--bg-subtle, #f8fafc)" stroke="var(--border, #e2e8f0)" />
                <text x="12" y="22" fill="var(--plumb, #10b981)" fontWeight="700" fontSize="11">4. Refactor</text>
                <text x="12" y="42" fill="var(--text, #0f172a)" fontSize="10" fontWeight="500">Parallel candidates</text>
                <text x="12" y="58" fill="var(--text-muted, #64748b)" fontSize="9">Hash-lock test guard</text>
                <text x="12" y="74" fill="var(--text-muted, #64748b)" fontSize="9">Super & Nano</text>
              </g>

              {/* Arrow */}
              <path d="M590 437 H602" stroke="var(--text-muted, #94a3b8)" strokeWidth="1.5" />

              {/* Stage 5 */}
              <g transform="translate(604, 390)">
                <rect width="115" height="95" rx="4" fill="var(--bg-subtle, #f8fafc)" stroke="var(--border, #e2e8f0)" />
                <text x="12" y="22" fill="var(--plumb, #10b981)" fontWeight="700" fontSize="11">5. Compare</text>
                <text x="12" y="42" fill="var(--text, #0f172a)" fontSize="10" fontWeight="500">Diff probes</text>
                <text x="12" y="58" fill="var(--text-muted, #64748b)" fontSize="9">Unseen inputs</text>
                <text x="12" y="74" fill="var(--text-muted, #64748b)" fontSize="9">Drift check</text>
              </g>

              {/* Arrow */}
              <path d="M726 437 H738" stroke="var(--text-muted, #94a3b8)" strokeWidth="1.5" />

              {/* Stage 6 */}
              <g transform="translate(740, 390)">
                <rect width="85" height="95" rx="4" fill="var(--bg-subtle, #f8fafc)" stroke="var(--plumb, #10b981)" strokeWidth="1.5" />
                <text x="8" y="22" fill="var(--plumb, #10b981)" fontWeight="700" fontSize="11">6. Dossier</text>
                <text x="8" y="42" fill="var(--text, #0f172a)" fontSize="10" fontWeight="500">evidence.json</text>
                <text x="8" y="58" fill="var(--text-muted, #64748b)" fontSize="9">refactor.patch</text>
                <text x="8" y="74" fill="var(--text-muted, #64748b)" fontSize="9">Verdict holds</text>
              </g>
            </svg>
          </div>

          <div className="drawer-details">
            <div className="detail-col">
              <h4>Three Layers of Defense</h4>
              <ul>
                <li><strong>Characterization Pins:</strong> Hermetic tests capturing legacy quirks before any editing begins.</li>
                <li><strong>AST Tripwires:</strong> Deterministic code mutations proving test strength exceeds 85%.</li>
                <li><strong>Differential Probing:</strong> Side-by-side execution on unseen inputs to catch rounding drift and ordering bugs.</li>
              </ul>
            </div>
            <div className="detail-col">
              <h4>Copy-on-Write Acceleration</h4>
              <p>
                Token Factory Sandboxes checkpoint the baseline environment once, allowing parallel forks to spawn in <strong>1.64 ms</strong> (an 11.2x speedup over cold container initialization).
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
