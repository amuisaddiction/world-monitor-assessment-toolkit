import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, Filter, AlertTriangle } from 'lucide-react';
import { apiClient } from '../api/client';
import { Finding } from '../types/api';
import clsx from 'clsx';

export default function Findings() {
  const navigate = useNavigate();
  const [findings, setFindings] = useState<Finding[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [severityFilter, setSeverityFilter] = useState('All');

  useEffect(() => {
    async function loadFindings() {
      try {
        const res = await apiClient.get<Finding[]>('/api/findings');
        setFindings(res.data);
      } catch (err: any) {
        setError(err.message || 'Failed to load findings');
      } finally {
        setLoading(false);
      }
    }
    loadFindings();
  }, []);

  const filteredFindings = findings.filter(f => {
    const matchesSearch = f.title.toLowerCase().includes(searchTerm.toLowerCase()) || 
                          f.category.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesSeverity = severityFilter === 'All' || f.severity === severityFilter;
    return matchesSearch && matchesSeverity;
  });

  if (loading) {
    return (
      <div className="flex justify-center mt-20">
        <div className="w-8 h-8 border-4 border-primaryBlue border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  if (error && !findings.length) {
    return (
      <div className="text-center mt-20">
        <AlertTriangle className="w-12 h-12 text-critical mx-auto mb-4" />
        <p className="text-critical">{error}</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <h1 className="text-2xl font-bold">Security Findings</h1>
        
        <div className="flex items-center space-x-4 w-full md:w-auto">
          <div className="relative flex-1 md:w-64">
            <Search className="w-4 h-4 absolute left-3 top-3 text-textSecondary" />
            <input 
              type="text" 
              placeholder="Search findings..." 
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full bg-secondaryBg border border-borderBg rounded-md pl-9 pr-4 py-2 text-sm focus:outline-none focus:border-primaryBlue"
            />
          </div>
          
          <div className="relative">
            <Filter className="w-4 h-4 absolute left-3 top-3 text-textSecondary" />
            <select 
              value={severityFilter}
              onChange={(e) => setSeverityFilter(e.target.value)}
              className="bg-secondaryBg border border-borderBg rounded-md pl-9 pr-4 py-2 text-sm appearance-none focus:outline-none focus:border-primaryBlue"
            >
              <option value="All">All Severities</option>
              <option value="Critical">Critical</option>
              <option value="High">High</option>
              <option value="Medium">Medium</option>
              <option value="Low">Low</option>
              <option value="Informational">Informational</option>
            </select>
          </div>
        </div>
      </div>

      <div className="bg-cardBg border border-borderBg rounded-lg overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-secondaryBg/50 text-textSecondary text-xs uppercase tracking-wider border-b border-borderBg">
                <th className="p-4 font-medium">ID</th>
                <th className="p-4 font-medium">Severity</th>
                <th className="p-4 font-medium">Title</th>
                <th className="p-4 font-medium">Category</th>
                <th className="p-4 font-medium">CVSS</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-borderBg">
              {filteredFindings.map((f) => (
                <tr 
                  key={f.finding_id} 
                  className="hover:bg-secondaryBg/30 cursor-pointer transition-colors"
                  onClick={() => navigate(`/findings/${f.finding_id}`)}
                >
                  <td className="p-4 text-sm font-mono text-textSecondary">{f.finding_id.substring(0,8)}</td>
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
                  <td className="p-4 font-medium text-sm">{f.title}</td>
                  <td className="p-4 text-textSecondary text-sm">{f.category}</td>
                  <td className="p-4 font-mono text-sm">{f.cvss_score.toFixed(1)}</td>
                </tr>
              ))}
              {filteredFindings.length === 0 && (
                <tr>
                  <td colSpan={5} className="p-8 text-center text-textSecondary">
                    No findings match your criteria.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
