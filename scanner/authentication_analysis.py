from typing import List
from scanner.finding import Finding, Evidence
from scanner.utils import make_safe_request

def analyze_authentication(target_url: str) -> List[Finding]:
    findings = []
    response = make_safe_request(f"{target_url.rstrip('/')}/api/config")
    if response is None or response.status_code != 200:
        return findings
    try:
        data = response.json()
    except Exception:
        return findings

    auth_config = data.get("authentication", {})
    if auth_config.get("enabled", False) and not auth_config.get("session_secure", True):
        findings.append(Finding(
            title="Insecure Session Configuration",
            description="Session is not secure.",
            category="Authentication",
            affected_component="Session Management",
            severity="Medium",
            cvss_score=5.3,
            evidence=[Evidence(description="Auth Config", data=auth_config)],
            impact="Tokens can be intercepted.",
            business_impact="Medium",
            root_cause="session_secure is false.",
            remediation="Set Secure flags on session cookies."
        ))
    return findings
