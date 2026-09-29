export async function fetchHealth() {
  const res = await fetch('/api/health');
  return res.json();
}

export async function fetchSpecimens() {
  const res = await fetch('/api/specimens');
  return res.json();
}

export async function fetchReplays() {
  const res = await fetch('/api/replays');
  return res.json();
}

export async function createRun(params: any) {
  const res = await fetch('/api/runs', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(params),
  });
  return res.json();
}

export async function cancelRun(id: string) {
  const res = await fetch(`/api/runs/${id}/cancel`, { method: 'POST' });
  return res.json();
}

export async function getRun(id: string) {
  const res = await fetch(`/api/runs/${id}`);
  return res.json();
}

export function subscribeToEvents(runId: string, onEvent: (event: any) => void, lastSeq?: number): EventSource {
  const url = `/api/runs/${runId}/events${lastSeq !== undefined ? `?lastSeq=${lastSeq}` : ''}`;
  const es = new EventSource(url);
  es.onmessage = (e) => onEvent(JSON.parse(e.data));
  return es;
}

export function subscribeToReplay(replayId: string, speed: number, onEvent: (event: any) => void): EventSource {
  const es = new EventSource(`/api/replays/${replayId}/events?speed=${speed}`);
  es.onmessage = (e) => onEvent(JSON.parse(e.data));
  return es;
}
