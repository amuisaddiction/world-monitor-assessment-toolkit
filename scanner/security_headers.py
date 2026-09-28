from typing import List
from scanner.finding import Finding, Evidence
from scanner.utils import make_safe_request

def analyze_security_headers(target_url: str) -> List[Finding]:
    findings = []
    response = make_safe_request(target_url)
    if response is None:
        return findings

    headers = {k.lower(): v for k, v in response.headers.items()}
    evidence_data = {"headers": dict(headers)}

    if "x-content-type-options" not in headers:
        findings.append(Finding(
            title="Missing X-Content-Type-Options Header",
            description="The X-Content-Type-Options header is missing.",
            category="Security Headers",
            affected_component=target_url,
            severity="Low",
            cvss_score=2.0,
            evidence=[Evidence(description="Response headers", data=evidence_data)],
            impact="Browsers may MIME-sniff the response.",
            business_impact="Low",
            root_cause="Server configuration missing header.",
            remediation="Set X-Content-Type-Options: nosniff"
        ))
    return findings
