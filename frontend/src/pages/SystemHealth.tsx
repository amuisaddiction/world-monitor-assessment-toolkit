import { Server, Database, Activity, Cpu, RotateCcw } from 'lucide-react';
import { useSystemHealth } from '../hooks/useSystemHealth';
import { apiClient } from '../api/client';
import { useState } from 'react';

export default function SystemHealth() {
  const { health, loading, error } = useSystemHealth();
  const [resetting, setResetting] = useState(false);
  const [resetMessage, setResetMessage] = useState('');

  const handleReset = async () => {
    if (!confirm('Are you sure you want to reset the environment? All findings will be cleared.')) return;
    setResetting(true);
    try {
      await apiClient.post('/api/reset');
      setResetMessage('Demo environment reset successfully.');
      setTimeout(() => window.location.reload(), 1500);
    } catch (err) {
      setResetMessage('Failed to reset environment.');
    } finally {
      setResetting(false);
    }
  };

  const isHealthy = health?.status === 'healthy';

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <h1 className="text-2xl font-bold">System Health</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Backend API */}
        <div className="bg-cardBg border border-borderBg p-6 rounded-lg flex items-start">
          <div className="p-3 bg-secondaryBg rounded-lg mr-4 border border-borderBg">
            <Server className="w-6 h-6 text-primaryBlue" />
          </div>
          <div>
            <h3 className="font-semibold text-lg mb-1">Backend API</h3>
            <p className="text-sm text-textSecondary mb-2">Primary orchestration and data service</p>
            <div className="flex items-center mt-2">
              <span className={`w-2.5 h-2.5 rounded-full mr-2 ${loading ? 'bg-warning animate-pulse' : isHealthy ? 'bg-success' : 'bg-critical'}`} />
              <span className="font-medium text-sm">
                {loading ? 'Checking...' : isHealthy ? 'Operational' : error ? 'Offline' : 'Degraded'}
              </span>
            </div>
          </div>
        </div>

        {/* Database */}
        <div className="bg-cardBg border border-borderBg p-6 rounded-lg flex items-start">
          <div className="p-3 bg-secondaryBg rounded-lg mr-4 border border-borderBg">
            <Database className="w-6 h-6 text-primaryBlue" />
          </div>
          <div>
            <h3 className="font-semibold text-lg mb-1">Database Layer</h3>
            <p className="text-sm text-textSecondary mb-2">Findings and evidence persistence</p>
            <div className="flex items-center mt-2">
              <span className={`w-2.5 h-2.5 rounded-full mr-2 ${loading ? 'bg-warning animate-pulse' : isHealthy ? 'bg-success' : 'bg-critical'}`} />
              <span className="font-medium text-sm">
                {loading ? 'Checking...' : isHealthy ? 'Operational' : 'Offline'}
              </span>
            </div>
          </div>
        </div>

        {/* Scanner Engine */}
        <div className="bg-cardBg border border-borderBg p-6 rounded-lg flex items-start">
          <div className="p-3 bg-secondaryBg rounded-lg mr-4 border border-borderBg">
            <Activity className="w-6 h-6 text-primaryBlue" />
          </div>
          <div>
            <h3 className="font-semibold text-lg mb-1">Scanner Engine</h3>
            <p className="text-sm text-textSecondary mb-2">Security analysis orchestrator</p>
            <div className="flex items-center mt-2">
              <span className={`w-2.5 h-2.5 rounded-full mr-2 ${loading ? 'bg-warning animate-pulse' : isHealthy ? 'bg-success' : 'bg-critical'}`} />
              <span className="font-medium text-sm">
                {loading ? 'Checking...' : isHealthy ? 'Operational' : 'Offline'}
              </span>
            </div>
          </div>
        </div>

        {/* AI Triage */}
        <div className="bg-cardBg border border-borderBg p-6 rounded-lg flex items-start">
          <div className="p-3 bg-secondaryBg rounded-lg mr-4 border border-borderBg">
            <Cpu className="w-6 h-6 text-primaryBlue" />
          </div>
          <div>
            <h3 className="font-semibold text-lg mb-1">AI Triage</h3>
            <p className="text-sm text-textSecondary mb-2">Automated report generation</p>
            <div className="flex items-center mt-2">
              <span className={`w-2.5 h-2.5 rounded-full mr-2 ${loading ? 'bg-warning animate-pulse' : isHealthy ? 'bg-success' : 'bg-critical'}`} />
              <span className="font-medium text-sm">
                {loading ? 'Checking...' : isHealthy ? 'Ready (Fallback/Gemini)' : 'Offline'}
              </span>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-cardBg border border-critical/30 p-6 rounded-lg mt-8">
        <h3 className="text-lg font-semibold text-critical mb-2">Demo Environment Controls</h3>
        <p className="text-sm text-textSecondary mb-4">
          Resetting the environment will purge all databases, findings, and evidence. 
          This is useful for starting a fresh demonstration.
        </p>
        <button 
          onClick={handleReset}
          disabled={resetting}
          className="bg-critical hover:bg-red-600 disabled:opacity-50 text-white px-4 py-2 rounded-md text-sm font-medium flex items-center transition-colors"
        >
          <RotateCcw className={`w-4 h-4 mr-2 ${resetting ? 'animate-spin' : ''}`} />
          {resetting ? 'Resetting...' : 'Reset Environment'}
        </button>
        {resetMessage && <p className="mt-3 text-sm text-textPrimary">{resetMessage}</p>}
      </div>
    </div>
  );
}
