import { useState, useEffect, useRef, useMemo } from 'react';
import { RunState, EventEnvelope } from './types';
import { reduceEvent, initialState } from './reducer';
import { subscribeToEvents, subscribeToReplay } from './api';

export function useRunStream(runId: string | null, isReplay = false, speed = 1) {
  const [events, setEvents] = useState<EventEnvelope[]>([]);
  const [scrubIndex, setScrubIndex] = useState<number | null>(null);
  const [error, setError] = useState<Error | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const lastSeq = useRef<number>(-1);

  useEffect(() => {
    if (!runId) return;

    setIsConnected(false);
    setError(null);
    setEvents([]);
    setScrubIndex(null);
    lastSeq.current = -1;

    let es: EventSource;

    const handleEvent = (event: EventEnvelope) => {
      lastSeq.current = event.seq;
      setEvents(prev => [...prev, event]);
    };

    try {
      if (isReplay) {
        es = subscribeToReplay(runId, speed, handleEvent);
      } else {
        es = subscribeToEvents(runId, handleEvent, lastSeq.current !== -1 ? lastSeq.current : undefined);
      }

      es.onopen = () => setIsConnected(true);
      es.onerror = () => {
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

  const state: RunState = useMemo(() => {
    const stream = scrubIndex !== null ? events.slice(0, scrubIndex) : events;
    return stream.reduce(reduceEvent, initialState);
  }, [events, scrubIndex]);

  return {
    state,
    error,
    isConnected,
    totalEvents: events.length,
    scrubIndex,
    setScrubIndex,
  };
}
