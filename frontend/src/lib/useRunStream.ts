import { useState, useEffect, useRef } from 'react';
import { RunState, EventEnvelope } from './types';
import { reduceEvent, initialState } from './reducer';
import { subscribeToEvents, subscribeToReplay } from './api';

export function useRunStream(runId: string | null, isReplay = false, speed = 1) {
  const [state, setState] = useState<RunState>(initialState);
  const [error, setError] = useState<Error | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const lastSeq = useRef<number>(-1);

  useEffect(() => {
    if (!runId) return;

    setIsConnected(false);
    setError(null);
    setState(initialState);

    let es: EventSource;

    const handleEvent = (event: EventEnvelope) => {
      lastSeq.current = event.seq;
      setState(prev => reduceEvent(prev, event));
    };

    try {
      if (isReplay) {
        es = subscribeToReplay(runId, speed, handleEvent);
      } else {
        es = subscribeToEvents(runId, handleEvent, lastSeq.current !== -1 ? lastSeq.current : undefined);
      }

      es.onopen = () => setIsConnected(true);
      es.onerror = (err) => {
        setIsConnected(false);
        setError(new Error('Event source connection error'));
      };
    } catch (err: any) {
      setError(err);
    }

    return () => {
      if (es) {
        es.close();
      }
    };
  }, [runId, isReplay, speed]);

  return { state, error, isConnected };
}
