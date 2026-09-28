from typing import List
from scanner.finding import Finding, Evidence
from scanner.utils import make_safe_request

def analyze_api_configuration(target_url: str) -> List[Finding]:
    findings = []
    response = make_safe_request(f"{target_url.rstrip('/')}/api/config")
    if response is None or response.status_code != 200:
        return findings
    try:
        data = response.json()
    except Exception:
        return findings

    auth_config = data.get("authentication", {})
    if not auth_config.get("enabled", True):
        findings.append(Finding(
            title="API Authentication Disabled",
            description="Authentication is explicitly disabled in API config.",
            category="API Security",
            affected_component="/api/config",
            severity="High",
            cvss_score=7.5,
            evidence=[Evidence(description="Config", data=data)],
            impact="Unauthenticated API access.",
            business_impact="High",
            root_cause="auth.enabled is false.",
            remediation="Enable authentication."
        ))
    return findings
