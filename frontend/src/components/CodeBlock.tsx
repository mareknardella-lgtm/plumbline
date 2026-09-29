import React, { useState } from 'react';
import './CodeBlock.css';
import { Copy, Check } from 'lucide-react';

interface CodeBlockProps {
  code: string;
  language?: string;
}

export default function CodeBlock({ code, language = 'typescript' }: CodeBlockProps) {
  const [copied, setCopied] = useState(false);

  const copyToClipboard = async () => {
    await navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="code-block-wrapper">
      <button className="code-copy-btn" onClick={copyToClipboard} aria-label="Copy code">
        {copied ? <Check size={16} /> : <Copy size={16} />}
      </button>
      <pre className="code-block">
        <code className={`language-${language}`}>
          {code}
        </code>
      </pre>
    </div>
  );
}
