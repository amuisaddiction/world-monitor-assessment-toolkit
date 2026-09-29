import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Shield, PlayCircle, Loader2 } from 'lucide-react';
import { apiClient } from '../api/client';

export default function NewAssessment() {
  const navigate = useNavigate();
  const [scanning, setScanning] = useState(false);
  const [progress, setProgress] = useState('');
  const [error, setError] = useState<string | null>(null);

  const startScan = async () => {
    setScanning(true);
    setError(null);
    setProgress('Initializing assessment...');
    
    try {
      // The API is hardcoded to accept "http://127.0.0.1:8080" as the internal target
      const res = await apiClient.post('/api/scans', { target_url: 'http://127.0.0.1:8080' });
      
      if (res.status === 200) {
        // Simulate progress for UI feedback since backend is async
        const steps = [
          "Discovery & Mapping...",
          "Evaluating Security Headers...",
          "Analyzing Authentication...",
          "Analyzing Authorization...",
          "Evaluating API Controls...",
          "Calculating Risk...",
          "Persisting Findings..."
        ];
        
        for (let i = 0; i < steps.length; i++) {
          await new Promise(r => setTimeout(r, 1200));
          setProgress(steps[i]);
        }
        
        navigate('/findings');
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to start assessment. Ensure the API is reachable.');
      setScanning(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-bold mb-2">New Security Assessment</h1>
        <p className="text-textSecondary">Initiate an authorized defensive security scan against the controlled environment.</p>
      </div>

      <div className="bg-cardBg border border-borderBg rounded-lg p-6">
        <div className="flex items-center mb-6">
          <Shield className="w-6 h-6 text-primaryBlue mr-3" />
          <h2 className="text-lg font-semibold">Assessment Configuration</h2>
        </div>
        
        <div className="space-y-4 mb-8">
          <div>
            <label className="block text-sm font-medium text-textSecondary mb-2">Target Environment</label>
            <input 
              type="text" 
              value="Internal Demo Target (Restricted)" 
              disabled 
              className="w-full bg-secondaryBg border border-borderBg rounded-md px-4 py-2 text-textPrimary cursor-not-allowed opacity-75"
            />
            <p className="text-xs text-textSecondary mt-2">
              Note: This platform is restricted to authorized internal targets only. Arbitrary public scanning is disabled.
            </p>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-textSecondary mb-2">Assessment Profile</label>
            <select disabled className="w-full bg-secondaryBg border border-borderBg rounded-md px-4 py-2 text-textPrimary cursor-not-allowed opacity-75">
              <option>Full Security Audit (Headers, API, Auth, Client)</option>
            </select>
          </div>
        </div>

        {error && (
          <div className="mb-6 p-4 bg-critical/10 border border-critical/30 rounded-md text-critical text-sm">
            {error}
          </div>
        )}

        <div className="pt-4 border-t border-borderBg flex justify-end">
          <button
            onClick={startScan}
            disabled={scanning}
            className="flex items-center bg-primaryBlue hover:bg-secondaryBlue disabled:opacity-50 disabled:cursor-not-allowed text-white px-6 py-2.5 rounded-md font-medium transition-colors"
          >
            {scanning ? (
              <>
                <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                {progress}
              </>
            ) : (
              <>
                <PlayCircle className="w-5 h-5 mr-2" />
                START SECURITY ASSESSMENT
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
