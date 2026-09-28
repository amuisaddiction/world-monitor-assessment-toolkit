from scanner.finding import Finding
from engine.cvss import calculate_risk

def assess_finding(finding: Finding) -> Finding:
    finding.severity = calculate_risk(finding.cvss_score)
    return finding
