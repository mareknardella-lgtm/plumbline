import React, { useState } from 'react';
import './DiffViewer.css';
import SegmentedControl from './SegmentedControl';
import Button from './Button';

interface DiffViewerProps {
  patch: string;
  isExercised?: boolean;
}

interface ParsedHunk {
  header: string;
  oldStart: number;
  newStart: number;
  lines: Array<{
    type: 'add' | 'del' | 'context' | 'meta';
    oldLine?: number;
    newLine?: number;
    text: string;
  }>;
}

export default function DiffViewer({ patch, isExercised = true }: DiffViewerProps) {
  const [mode, setMode] = useState<'unified' | 'split'>('unified');
  const [copied, setCopied] = useState(false);
  const [wrap, setWrap] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(patch);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // Fallback if clipboard API restricted
    }
  };

  // Parse git diff hunks
  const parseDiff = (raw: string): { files: string[]; hunks: ParsedHunk[] } => {
    const rawLines = raw.split('\n');
    const files: string[] = [];
    const hunks: ParsedHunk[] = [];

    let currentHunk: ParsedHunk | null = null;
    let oldLine = 0;
    let newLine = 0;

    for (const line of rawLines) {
      if (line.startsWith('--- ') || line.startsWith('+++ ')) {
        files.push(line);
      } else if (line.startsWith('@@ ')) {
        const match = line.match(/@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@(.*)/);
        if (match && match[1] && match[2]) {
          oldLine = parseInt(match[1], 10);
          newLine = parseInt(match[2], 10);
          currentHunk = {
            header: line,
            oldStart: oldLine,
            newStart: newLine,
            lines: [],
          };
          hunks.push(currentHunk);
        }
      } else if (currentHunk) {
        if (line.startsWith('+')) {
          currentHunk.lines.push({
            type: 'add',
            newLine: newLine++,
            text: line.slice(1),
          });
        } else if (line.startsWith('-')) {
          currentHunk.lines.push({
            type: 'del',
            oldLine: oldLine++,
            text: line.slice(1),
          });
        } else {
          currentHunk.lines.push({
            type: 'context',
            oldLine: oldLine++,
            newLine: newLine++,
            text: line.startsWith(' ') ? line.slice(1) : line,
          });
        }
      }
    }

    return { files, hunks };
  };

  const { hunks } = parseDiff(patch);

  return (
    <div className="diff-viewer">
      <div className="diff-header">
        <div className="diff-header-left">
          <span className="diff-title">The Verified Change</span>
          {isExercised ? (
            <span className="hunk-badge exercised">✓ Exercised by pins</span>
          ) : (
            <span className="hunk-badge unexercised">⚠ Not exercised</span>
          )}
        </div>
        <div className="diff-header-actions">
          <button
            type="button"
            className={`diff-tool-btn ${wrap ? 'active' : ''}`}
            onClick={() => setWrap(!wrap)}
            title="Toggle line wrapping"
          >
            Wrap
          </button>
          <Button variant="quiet" size="sm" onClick={handleCopy}>
            {copied ? '✓ Copied' : 'Copy patch'}
          </Button>
          <SegmentedControl
            options={[
              { label: 'Unified', value: 'unified' },
              { label: 'Split', value: 'split' },
            ]}
            value={mode}
            onChange={(val) => setMode(val as 'unified' | 'split')}
          />
        </div>
      </div>

      <div className={`diff-content diff-${mode} ${wrap ? 'wrap-lines' : ''}`}>
        {hunks.length === 0 ? (
          <pre className="raw-diff">{patch}</pre>
        ) : mode === 'unified' ? (
          <div className="unified-diff-table">
            {hunks.map((hunk, hIdx) => (
              <div key={hIdx} className="diff-hunk">
                <div className="diff-hunk-header">
                  <span className="hunk-range">{hunk.header}</span>
                  <span className="hunk-meta">Hunk {hIdx + 1}</span>
                </div>
                {hunk.lines.map((l, lIdx) => (
                  <div key={lIdx} className={`diff-row diff-row-${l.type}`}>
                    <span className="line-num old-num">{l.oldLine ?? ''}</span>
                    <span className="line-num new-num">{l.newLine ?? ''}</span>
                    <span className="line-prefix">
                      {l.type === 'add' ? '+' : l.type === 'del' ? '-' : ' '}
                    </span>
                    <span className="line-text">{l.text || ' '}</span>
                  </div>
                ))}
              </div>
            ))}
          </div>
        ) : (
          <div className="split-diff-table">
            {hunks.map((hunk, hIdx) => (
              <div key={hIdx} className="diff-hunk-split">
                <div className="diff-hunk-header">
                  <span className="hunk-range">{hunk.header}</span>
                  <span className="hunk-meta">Hunk {hIdx + 1}</span>
                </div>
                <div className="split-rows">
                  {hunk.lines.map((l, lIdx) => (
                    <div key={lIdx} className={`split-row split-${l.type}`}>
                      <div className={`split-pane split-left ${l.type === 'del' ? 'del' : ''}`}>
                        <span className="line-num">{l.type !== 'add' ? l.oldLine : ''}</span>
                        <span className="line-text">
                          {l.type !== 'add' ? (l.type === 'del' ? `- ${l.text}` : `  ${l.text}`) : ''}
                        </span>
                      </div>
                      <div className={`split-pane split-right ${l.type === 'add' ? 'add' : ''}`}>
                        <span className="line-num">{l.type !== 'del' ? l.newLine : ''}</span>
                        <span className="line-text">
                          {l.type !== 'del' ? (l.type === 'add' ? `+ ${l.text}` : `  ${l.text}`) : ''}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
