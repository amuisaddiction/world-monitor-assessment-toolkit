from ai_triage.fallback import generate_local_fallback_report

def test_fallback_no_findings():
    report = generate_local_fallback_report([])
    assert "No security findings were generated" in report

def test_fallback_with_findings():
    findings = [{"title": "XSS", "severity": "High", "cvss_score": 7.5}]
    report = generate_local_fallback_report(findings)
    assert "XSS" in report
    assert "High" in report
