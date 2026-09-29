import React from 'react';
import Button from '../components/Button';

interface ReplayBannerProps {
  date: string;
  onStartOwnRun: () => void;
}

export default function ReplayBanner({ date, onStartOwnRun }: ReplayBannerProps) {
  return (
    <div style={{
      background: '#fef3c7',
      color: '#92400e',
      padding: '12px 24px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      fontWeight: 500
    }}>
      <span>Replay of a live run recorded on {date}. Nothing is running now.</span>
      <Button variant="primary" size="sm" onClick={onStartOwnRun}>Start own run</Button>
    </div>
  );
}
