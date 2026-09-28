import pytest
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
