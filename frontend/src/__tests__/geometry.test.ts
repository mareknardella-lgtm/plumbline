import { computeGraphLayout } from '../geometry';

describe('geometry', () => {
  it('should compute basic layout without candidates', () => {
    const layout = computeGraphLayout({ candidates: [] } as any, 500, 500);
    expect(layout.anchor).toEqual({ x: 250, y: 20 });
    expect(layout.baselineX).toBe(250);
  });
});
