from typing import List
from scanner.finding import Finding, Evidence
from scanner.utils import make_safe_request

def analyze_client_security(target_url: str) -> List[Finding]:
    findings = []
    response = make_safe_request(f"{target_url.rstrip('/')}/api/config")
    if response is None or response.status_code != 200:
        return findings
    try:
        data = response.json()
    except Exception:
        return findings

    headers = data.get("headers", {})
    if not headers.get("strict_transport_security", True):
        findings.append(Finding(
            title="Missing HSTS in Client Config",
            description="Client config missing HSTS.",
            category="Client Security",
            affected_component="Headers",
            severity="Medium",
            cvss_score=4.3,
            evidence=[Evidence(description="Headers", data=headers)],
            impact="Downgrade attacks.",
            business_impact="Medium",
            root_cause="HSTS missing.",
            remediation="Enable HSTS."
        ))
    return findings
