import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ShieldAlert, AlertTriangle, Info, CheckCircle, Clock } from 'lucide-react';
import { apiClient } from '../api/client';
import { ScanResponse, Finding } from '../types/api';
import clsx from 'clsx';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip as RechartsTooltip, BarChart, Bar, XAxis, YAxis } from 'recharts';

export default function Overview() {
  const navigate = useNavigate();
  const [scans, setScans] = useState<ScanResponse[]>([]);
  const [findings, setFindings] = useState<Finding[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchData() {
      try {
        const [scansRes, findingsRes] = await Promise.all([
          apiClient.get<ScanResponse[]>('/api/scans'),
          apiClient.get<Finding[]>('/api/findings')
        ]);
        setScans(scansRes.data);
        setFindings(findingsRes.data);
      } catch (err) {
        setError('Failed to load dashboard data. API may be offline.');
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center h-full space-y-4">
        <div className="w-8 h-8 border-4 border-primaryBlue border-t-transparent rounded-full animate-spin" />
        <p className="text-textSecondary">Loading dashboard...</p>
      </div>
    );
  }

  if (error && !scans.length && !findings.length) {
    return (
      <div className="bg-cardBg border border-critical/50 p-6 rounded-lg text-center">
        <AlertTriangle className="w-12 h-12 text-critical mx-auto mb-4" />
        <h2 className="text-xl font-bold mb-2">API Connection Failed</h2>
        <p className="text-textSecondary mb-4">{error}</p>
        <button onClick={() => window.location.reload()} className="bg-primaryBlue hover:bg-secondaryBlue text-white px-4 py-2 rounded transition-colors">
          Retry Connection
        </button>
      </div>
    );
  }

  if (scans.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-center max-w-lg mx-auto">
        <ShieldAlert className="w-16 h-16 text-textSecondary mb-6" />
        <h2 className="text-2xl font-bold mb-2">No Assessments Found</h2>
        <p className="text-textSecondary mb-8">
          The World Monitor Security Assessment Center has not executed any scans yet. Start your first authorized assessment to populate the dashboard.
        </p>
        <button
          onClick={() => navigate('/assessment')}
          className="bg-primaryBlue hover:bg-secondaryBlue text-white px-6 py-3 rounded font-medium transition-colors"
        >
          START NEW ASSESSMENT
        </button>
      </div>
    );
  }

  const latestScan = scans[0];
  
  // Derived metrics
  const critical = findings.filter(f => f.severity === 'Critical').length;
  const high = findings.filter(f => f.severity === 'High').length;
  const medium = findings.filter(f => f.severity === 'Medium').length;
  const low = findings.filter(f => f.severity === 'Low').length;
  const info = findings.filter(f => f.severity === 'Informational').length;

  const severityData = [
    { name: 'Critical', value: critical, color: '#EF4444' },
    { name: 'High', value: high, color: '#F97316' },
    { name: 'Medium', value: medium, color: '#F59E0B' },
    { name: 'Low', value: low, color: '#3B82F6' },
    { name: 'Info', value: info, color: '#64748B' },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Executive Overview</h1>
        <div className="flex items-center text-sm text-textSecondary bg-cardBg px-4 py-2 rounded-md border border-borderBg">
          <Clock className="w-4 h-4 mr-2" />
          Latest Scan: {latestScan.id.substring(0,8)} ({latestScan.status})
        </div>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        <div className="bg-cardBg border border-borderBg p-4 rounded-lg">
          <p className="text-sm font-medium text-textSecondary">Total Findings</p>
          <p className="text-3xl font-bold mt-2">{findings.length}</p>
        </div>
        <div className="bg-cardBg border border-critical/30 p-4 rounded-lg">
          <p className="text-sm font-medium text-critical">Critical</p>
          <p className="text-3xl font-bold mt-2 text-critical">{critical}</p>
        </div>
        <div className="bg-cardBg border border-orange-500/30 p-4 rounded-lg">
          <p className="text-sm font-medium text-orange-500">High</p>
          <p className="text-3xl font-bold mt-2 text-orange-500">{high}</p>
        </div>
        <div className="bg-cardBg border border-warning/30 p-4 rounded-lg">
          <p className="text-sm font-medium text-warning">Medium</p>
          <p className="text-3xl font-bold mt-2 text-warning">{medium}</p>
        </div>
        <div className="bg-cardBg border border-blue-500/30 p-4 rounded-lg">
          <p className="text-sm font-medium text-blue-500">Low</p>
          <p className="text-3xl font-bold mt-2 text-blue-500">{low}</p>
        </div>
        <div className="bg-cardBg border border-slate-500/30 p-4 rounded-lg">
          <p className="text-sm font-medium text-slate-400">Informational</p>
          <p className="text-3xl font-bold mt-2 text-slate-400">{info}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-cardBg border border-borderBg rounded-lg p-6">
          <h3 className="text-lg font-semibold mb-4">Severity Distribution</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={severityData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <XAxis dataKey="name" stroke="#94A3B8" fontSize={12} />
                <YAxis stroke="#94A3B8" fontSize={12} />
                <RechartsTooltip cursor={{ fill: '#263247' }} contentStyle={{ backgroundColor: '#172033', borderColor: '#263247', color: '#F8FAFC' }} />
                <Bar dataKey="value" radius={[4, 4, 0, 0]}>
                  {severityData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
        
        <div className="bg-cardBg border border-borderBg rounded-lg p-6">
          <h3 className="text-lg font-semibold mb-4">Risk Composition</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={severityData.filter(d => d.value > 0)}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={90}
                  paddingAngle={2}
                  dataKey="value"
                >
                  {severityData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <RechartsTooltip contentStyle={{ backgroundColor: '#172033', borderColor: '#263247', color: '#F8FAFC' }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Recent Findings Table */}
      <div className="bg-cardBg border border-borderBg rounded-lg overflow-hidden">
        <div className="p-4 border-b border-borderBg flex justify-between items-center">
          <h3 className="text-lg font-semibold">Recent Findings</h3>
          <button onClick={() => navigate('/findings')} className="text-sm text-primaryBlue hover:underline">View All</button>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-secondaryBg/50 text-textSecondary text-xs uppercase tracking-wider">
                <th className="p-4 font-medium">Severity</th>
                <th className="p-4 font-medium">Title</th>
                <th className="p-4 font-medium">Category</th>
                <th className="p-4 font-medium">CVSS</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-borderBg">
              {findings.slice(0, 5).map((f) => (
                <tr key={f.finding_id} className="hover:bg-secondaryBg/30 cursor-pointer" onClick={() => navigate(`/findings/${f.finding_id}`)}>
                  <td className="p-4">
                    <span className={clsx("px-2.5 py-1 text-xs font-semibold rounded-full", {
                      'bg-critical/20 text-critical': f.severity === 'Critical',
                      'bg-orange-500/20 text-orange-500': f.severity === 'High',
                      'bg-warning/20 text-warning': f.severity === 'Medium',
                      'bg-blue-500/20 text-blue-500': f.severity === 'Low',
                      'bg-slate-500/20 text-slate-300': f.severity === 'Informational',
                    })}>
                      {f.severity}
                    </span>
                  </td>
                  <td className="p-4 font-medium">{f.title}</td>
                  <td className="p-4 text-textSecondary">{f.category}</td>
                  <td className="p-4 text-textSecondary">{f.cvss_score.toFixed(1)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
