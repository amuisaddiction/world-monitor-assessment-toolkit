import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, ShieldAlert } from 'lucide-react';
import { apiClient } from '../api/client';
import { Finding } from '../types/api';
import clsx from 'clsx';

export default function FindingDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [finding, setFinding] = useState<Finding | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchFinding() {
      try {
        const res = await apiClient.get<Finding>(`/api/findings/${id}`);
        setFinding(res.data);
      } catch (err: any) {
        setError('Failed to load finding details.');
      } finally {
        setLoading(false);
      }
    }
    fetchFinding();
  }, [id]);

  if (loading) {
    return <div className="p-8 text-center"><div className="w-8 h-8 border-4 border-primaryBlue border-t-transparent rounded-full animate-spin mx-auto" /></div>;
  }

  if (error || !finding) {
    return <div className="text-critical">{error || 'Finding not found'}</div>;
  }

  return (
    <div className="max-w-4xl space-y-6">
      <button onClick={() => navigate(-1)} className="flex items-center text-textSecondary hover:text-textPrimary transition-colors">
        <ArrowLeft className="w-4 h-4 mr-2" /> Back to Findings
      </button>

      <div className="bg-cardBg border border-borderBg rounded-lg overflow-hidden">
        <div className="p-6 border-b border-borderBg flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold mb-2">{finding.title}</h1>
            <p className="font-mono text-sm text-textSecondary">ID: {finding.finding_id}</p>
          </div>
          <div className="flex gap-3">
            <span className={clsx("px-3 py-1 text-sm font-semibold rounded-full border", {
              'bg-critical/20 text-critical border-critical/50': finding.severity === 'Critical',
              'bg-orange-500/20 text-orange-500 border-orange-500/50': finding.severity === 'High',
              'bg-warning/20 text-warning border-warning/50': finding.severity === 'Medium',
              'bg-blue-500/20 text-blue-500 border-blue-500/50': finding.severity === 'Low',
              'bg-slate-500/20 text-slate-300 border-slate-500/50': finding.severity === 'Informational',
            })}>
              {finding.severity}
            </span>
            <span className="px-3 py-1 text-sm font-bold bg-secondaryBg border border-borderBg rounded-full">
              CVSS: {finding.cvss_score.toFixed(1)}
            </span>
          </div>
        </div>

        <div className="p-6 space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 className="text-sm font-medium text-textSecondary uppercase mb-1">Category</h3>
              <p className="text-lg">{finding.category}</p>
            </div>
          </div>

          <div>
            <h3 className="text-sm font-medium text-textSecondary uppercase mb-2">Description</h3>
            <div className="bg-secondaryBg/50 p-4 rounded-md text-sm leading-relaxed border border-borderBg/50">
              {finding.description}
            </div>
          </div>

          <div>
            <h3 className="text-sm font-medium text-textSecondary uppercase mb-2">Impact</h3>
            <div className="bg-secondaryBg/50 p-4 rounded-md text-sm leading-relaxed border border-borderBg/50">
              {finding.impact}
            </div>
          </div>

          <div>
            <h3 className="text-sm font-medium text-textSecondary uppercase mb-2">Remediation Guidance</h3>
            <div className="bg-blue-900/10 border border-blue-900/30 p-4 rounded-md text-sm leading-relaxed">
              {finding.remediation}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
