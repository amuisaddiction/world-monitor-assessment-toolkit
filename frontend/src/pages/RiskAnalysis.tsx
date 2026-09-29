import { useState, useEffect } from 'react';
import { apiClient } from '../api/client';
import { Finding } from '../types/api';
import { BarChart, Bar, XAxis, YAxis, ResponsiveContainer, Tooltip, Cell } from 'recharts';

export default function RiskAnalysis() {
  const [findings, setFindings] = useState<Finding[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchFindings() {
      try {
        const res = await apiClient.get<Finding[]>('/api/findings');
        setFindings(res.data);
      } catch (err) {
        // handle error
      } finally {
        setLoading(false);
      }
    }
    fetchFindings();
  }, []);

  if (loading) return <div>Loading Risk Analytics...</div>;

  const categories = findings.reduce((acc, f) => {
    acc[f.category] = (acc[f.category] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  const categoryData = Object.entries(categories).map(([name, value]) => ({ name, value }));
  const maxCvss = findings.length > 0 ? Math.max(...findings.map(f => f.cvss_score)) : 0;
  const avgCvss = findings.length > 0 ? (findings.reduce((acc, f) => acc + f.cvss_score, 0) / findings.length).toFixed(1) : 0;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Risk Analytics</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-cardBg border border-borderBg p-6 rounded-lg text-center">
          <p className="text-textSecondary uppercase text-sm mb-2">Max CVSS Score</p>
          <p className="text-4xl font-bold text-critical">{maxCvss.toFixed(1)}</p>
        </div>
        <div className="bg-cardBg border border-borderBg p-6 rounded-lg text-center">
          <p className="text-textSecondary uppercase text-sm mb-2">Average CVSS Score</p>
          <p className="text-4xl font-bold text-warning">{avgCvss}</p>
        </div>
        <div className="bg-cardBg border border-borderBg p-6 rounded-lg text-center">
          <p className="text-textSecondary uppercase text-sm mb-2">Affected Categories</p>
          <p className="text-4xl font-bold text-primaryBlue">{categoryData.length}</p>
        </div>
      </div>

      <div className="bg-cardBg border border-borderBg rounded-lg p-6">
        <h3 className="text-lg font-semibold mb-6">Findings by Category</h3>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={categoryData} layout="vertical" margin={{ left: 100 }}>
              <XAxis type="number" stroke="#94A3B8" />
              <YAxis dataKey="name" type="category" stroke="#94A3B8" width={150} />
              <Tooltip cursor={{ fill: '#263247' }} contentStyle={{ backgroundColor: '#172033', borderColor: '#263247', color: '#F8FAFC' }} />
              <Bar dataKey="value" fill="#3B82F6" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
