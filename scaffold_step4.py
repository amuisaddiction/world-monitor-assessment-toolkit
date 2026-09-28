import os

workspace = "c:/Users/ankit/Downloads/world-monitor-security-assessment 2"

files = {
    "scanner/__init__.py": "",
    "engine/__init__.py": "",
    "tests/__init__.py": "",
    "scanner/utils.py": """import httpx
import logging
import re
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def make_safe_request(url: str, method: str = "GET", timeout: int = 5) -> Optional[httpx.Response]:
    try:
        with httpx.Client(verify=False, timeout=timeout) as client:
            return client.request(method, url)
    except httpx.RequestError as exc:
        logger.error(f"Error requesting {exc.request.url!r}: {exc}")
        return None

def redact_secrets(data: str) -> str:
    redacted = re.sub(r"(Bearer\s+)[A-Za-z0-9\-\._~]+", r"\\1[REDACTED]", data)
    return redacted
""",
    "scanner/security_headers.py": """from typing import List
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
""",
    "scanner/api_analysis.py": """from typing import List
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
""",
    "scanner/authentication_analysis.py": """from typing import List
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
""",
    "scanner/authorization_analysis.py": """from typing import List
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
""",
    "scanner/client_security.py": """from typing import List
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
""",
    "engine/cvss.py": """def calculate_risk(base_score: float) -> str:
    if base_score < 4.0:
        return "Low"
    if base_score < 7.0:
        return "Medium"
    if base_score < 9.0:
        return "High"
    return "Critical"
""",
    "engine/risk_engine.py": """from scanner.finding import Finding
from engine.cvss import calculate_risk

def assess_finding(finding: Finding) -> Finding:
    finding.severity = calculate_risk(finding.cvss_score)
    return finding
""",
    "engine/correlation.py": """from typing import List
from scanner.finding import Finding

def deduplicate_findings(findings: List[Finding]) -> List[Finding]:
    unique = {}
    for f in findings:
        key = f"{f.category}-{f.title}-{f.affected_component}"
        if key not in unique or f.cvss_score > unique[key].cvss_score:
            unique[key] = f
    return list(unique.values())
""",
    "tests/test_all.py": """import pytest
from scanner.security_headers import analyze_security_headers
from scanner.api_analysis import analyze_api_configuration
from scanner.authentication_analysis import analyze_authentication
from scanner.authorization_analysis import analyze_authorization
from scanner.client_security import analyze_client_security
from engine.cvss import calculate_risk
from engine.correlation import deduplicate_findings
from scanner.finding import Finding

TARGET = "http://127.0.0.1:8080"

def test_security_headers():
    findings = analyze_security_headers(TARGET)
    assert isinstance(findings, list)

def test_api_analysis():
    findings = analyze_api_configuration(TARGET)
    assert isinstance(findings, list)

def test_authentication_analysis():
    findings = analyze_authentication(TARGET)
    assert isinstance(findings, list)

def test_authorization_analysis():
    findings = analyze_authorization(TARGET)
    assert isinstance(findings, list)

def test_client_security():
    findings = analyze_client_security(TARGET)
    assert isinstance(findings, list)

def test_cvss():
    assert calculate_risk(3.9) == "Low"
    assert calculate_risk(6.9) == "Medium"
    assert calculate_risk(8.9) == "High"
    assert calculate_risk(9.5) == "Critical"

def test_correlation():
    f1 = Finding(title="A", description="A", category="C", affected_component="X", severity="Low", impact="", business_impact="", root_cause="", remediation="")
    f2 = Finding(title="A", description="A", category="C", affected_component="X", severity="High", cvss_score=8.0, impact="", business_impact="", root_cause="", remediation="")
    deduped = deduplicate_findings([f1, f2])
    assert len(deduped) == 1
    assert deduped[0].cvss_score == 8.0
"""
}

for path, content in files.items():
    full_path = os.path.join(workspace, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
print("Files generated successfully.")
