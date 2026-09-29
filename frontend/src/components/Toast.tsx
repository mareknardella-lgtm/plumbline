import React, { useState, useEffect } from 'react';
import './Toast.css';
import { X } from 'lucide-react';

interface ToastProps {
  message: string;
  onClose: () => void;
  duration?: number;
}

export default function Toast({ message, onClose, duration = 3000 }: ToastProps) {
  useEffect(() => {
    const timer = setTimeout(() => {
      onClose();
    }, duration);
    return () => clearTimeout(timer);
  }, [duration, onClose]);

  return (
    <div className="toast" role="alert">
      <span>{message}</span>
      <button onClick={onClose} aria-label="Close" className="toast-close">
        <X size={16} />
      </button>
    </div>
  );
}
