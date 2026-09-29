export interface Finding {
  finding_id: string;
  title: string;
  severity: string;
  category: string;
  description: string;
  impact: string;
  remediation: string;
  cvss_score: number;
}

export interface ScanResponse {
  id: string;
  target: string;
  status: string;
}

export interface ScanDetail extends ScanResponse {
  total_findings: number;
  critical_count: number;
  high_count: number;
  medium_count: number;
  low_count: number;
  informational_count: number;
}

export interface ReportResponse {
  id: string;
  scan_id: string;
  file_path: string;
}

export interface HealthResponse {
  status: string;
  service: string;
}
