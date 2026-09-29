import React from 'react';
import './Button.css';
import { Loader2 } from 'lucide-react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'quiet';
  size?: 'sm' | 'md';
  loading?: boolean;
}

export default function Button({ variant = 'primary', size = 'md', loading, children, className = '', disabled, ...props }: ButtonProps) {
  const classes = `btn btn-${variant} btn-${size} ${loading ? 'loading' : ''} ${className}`;
  
  return (
    <button className={classes} disabled={disabled || loading} {...props}>
      {loading && <Loader2 className="btn-spinner" size={16} />}
      <span className="btn-content">{children}</span>
    </button>
  );
}
