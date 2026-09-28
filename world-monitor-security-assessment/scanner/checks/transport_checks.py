"""
Secure communication checks: HTTPS enforcement, HSTS.
"""
from utils.http_client import get, new_finding


def run(target: str) -> list[dict]:
    findings = []

    if target.startswith("http://"):
        findings.append(new_finding(
            finding_id="TRANSPORT-001",
            title="Target served over plain HTTP",
            category="transport",
            severity="high",
            cvss_score=7.4,
            affected_component=target,
            description="The application is accessible over unencrypted HTTP.",
            reproduction_steps=[f"Access {target} and confirm no automatic redirect to HTTPS"],
            remediation="Enforce HTTPS everywhere; redirect all HTTP traffic to HTTPS.",
        ))
        return findings  # HSTS check below is only meaningful over HTTPS

    try:
        resp = get(target)
        if "strict-transport-security" not in {k.lower() for k in resp.headers.keys()}:
            findings.append(new_finding(
                finding_id="TRANSPORT-002",
                title="Missing HSTS header",
                category="transport",
                severity="low",
                cvss_score=3.1,
                affected_component=target,
                description="No Strict-Transport-Security header was found.",
                reproduction_steps=[f"Inspect response headers for {target}"],
                remediation="Add Strict-Transport-Security with an appropriate max-age and includeSubDomains.",
            ))
    except Exception:
        pass

    return findings
