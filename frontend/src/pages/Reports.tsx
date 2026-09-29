import { useState, useEffect } from 'react';
import { FileText, Download, Loader2 } from 'lucide-react';
import { apiClient } from '../api/client';
import { ScanResponse, ReportResponse } from '../types/api';

export default function Reports() {
  const [scans, setScans] = useState<ScanResponse[]>([]);
  const [reports, setReports] = useState<ReportResponse[]>([]);
  const [selectedScan, setSelectedScan] = useState<string>('');
  const [generating, setGenerating] = useState(false);
  const [message, setMessage] = useState<{type: 'success'|'error', text: string} | null>(null);

  useEffect(() => {
    async function loadScans() {
      try {
        const res = await apiClient.get<ScanResponse[]>('/api/scans');
        setScans(res.data);
        if (res.data.length > 0) {
          setSelectedScan(res.data[0].id);
          fetchReports(res.data[0].id);
        }
      } catch (err) {}
    }
    loadScans();
  }, []);

  const fetchReports = async (scanId: string) => {
    try {
      const res = await apiClient.get<ReportResponse[]>(`/api/reports/${scanId}`);
      setReports(res.data);
    } catch (err) {}
  };

  const handleScanChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const id = e.target.value;
    setSelectedScan(id);
    fetchReports(id);
  };

  const generateReport = async () => {
    if (!selectedScan) return;
    setGenerating(true);
    setMessage(null);
    try {
      await apiClient.post(`/api/reports/${selectedScan}`);
      setMessage({ type: 'success', text: 'Report generated successfully.' });
      fetchReports(selectedScan);
    } catch (err) {
      setMessage({ type: 'error', text: 'Failed to generate report.' });
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <h1 className="text-2xl font-bold">Assessment Reports</h1>

      <div className="bg-cardBg border border-borderBg rounded-lg p-6">
        <h2 className="text-lg font-semibold mb-4">Generate Report</h2>
        <div className="flex gap-4 items-end">
          <div className="flex-1">
            <label className="block text-sm font-medium text-textSecondary mb-2">Select Assessment</label>
            <select 
              value={selectedScan} 
              onChange={handleScanChange}
              className="w-full bg-secondaryBg border border-borderBg rounded-md px-4 py-2 text-textPrimary focus:outline-none focus:border-primaryBlue"
            >
              <option value="" disabled>Select an assessment</option>
              {scans.map(s => (
                <option key={s.id} value={s.id}>{s.id.substring(0,8)} - {s.target}</option>
              ))}
            </select>
          </div>
          <button 
            onClick={generateReport}
            disabled={!selectedScan || generating}
            className="bg-primaryBlue hover:bg-secondaryBlue disabled:opacity-50 text-white px-6 py-2 rounded-md font-medium flex items-center transition-colors"
          >
            {generating ? <Loader2 className="w-5 h-5 mr-2 animate-spin" /> : <FileText className="w-5 h-5 mr-2" />}
            Generate Report
          </button>
        </div>

        {message && (
          <div className={`mt-4 p-3 rounded-md text-sm ${message.type === 'success' ? 'bg-success/10 text-success border border-success/30' : 'bg-critical/10 text-critical border border-critical/30'}`}>
            {message.text}
          </div>
        )}
      </div>

      <div className="bg-cardBg border border-borderBg rounded-lg overflow-hidden">
        <div className="p-4 border-b border-borderBg">
          <h3 className="text-lg font-semibold">Available Reports</h3>
        </div>
        <div className="p-4">
          {reports.length === 0 ? (
            <p className="text-textSecondary text-center py-8">No reports generated for this assessment.</p>
          ) : (
            <div className="space-y-3">
              {reports.map(r => (
                <div key={r.id} className="flex items-center justify-between p-4 bg-secondaryBg rounded border border-borderBg">
                  <div className="flex items-center">
                    <FileText className="w-5 h-5 text-primaryBlue mr-3" />
                    <div>
                      <p className="font-medium text-sm">Security Assessment Report</p>
                      <p className="text-xs text-textSecondary font-mono">{r.file_path}</p>
                    </div>
                  </div>
                  <button className="text-textSecondary hover:text-primaryBlue flex items-center text-sm transition-colors">
                    <Download className="w-4 h-4 mr-1" /> Download
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
