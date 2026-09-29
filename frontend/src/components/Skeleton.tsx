import React from 'react';
import './Skeleton.css';

interface SkeletonProps {
  width?: string | number;
  height?: string | number;
  borderRadius?: string | number;
}

export default function Skeleton({ width = '100%', height = '20px', borderRadius = '4px' }: SkeletonProps) {
  return (
    <div className="skeleton" style={{ width, height, borderRadius }} />
  );
}
