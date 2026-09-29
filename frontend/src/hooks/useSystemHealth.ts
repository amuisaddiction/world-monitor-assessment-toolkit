import { useState, useEffect } from 'react';
import { apiClient } from '../api/client';
import { HealthResponse } from '../types/api';

export function useSystemHealth() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const checkHealth = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await apiClient.get<HealthResponse>('/health');
      setHealth(res.data);
    } catch (err: any) {
      setError(err.message || 'Failed to connect to backend API');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    checkHealth();
  }, []);

  return { health, loading, error, retry: checkHealth };
}
