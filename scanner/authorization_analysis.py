from typing import List
from scanner.finding import Finding, Evidence
from scanner.utils import make_safe_request

def analyze_authorization(target_url: str) -> List[Finding]:
    findings = []
    response = make_safe_request(f"{target_url.rstrip('/')}/api/config")
    if response is None or response.status_code != 200:
        return findings
    try:
        data = response.json()
    except Exception:
        return findings

    authz_config = data.get("authorization", {})
    if authz_config.get("broken_access_control_demo", False):
        findings.append(Finding(
            title="Broken Access Control Configured",
            description="Declarative config shows broken access control.",
            category="Authorization",
            affected_component="RBAC",
            severity="High",
            cvss_score=8.1,
            evidence=[Evidence(description="Authz Config", data=authz_config)],
            impact="Unauthorized access.",
            business_impact="High",
            root_cause="Demo flag enabled.",
            remediation="Enforce strict RBAC."
        ))
    return findings
