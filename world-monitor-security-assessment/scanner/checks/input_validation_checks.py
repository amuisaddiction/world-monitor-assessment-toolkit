"""
Input validation checks (XSS, SQLi, injection surfaces).

This module intentionally does NOT ship live attack payloads — build your
own test payloads manually per the OWASP Testing Guide once you've mapped
input fields during recon, and verify with Burp Suite/OWASP ZAP. Automating
raw injection payloads against a target you don't fully control yet is easy
to get wrong; do this step with manual review.

Use this module to record findings you've manually confirmed.
"""
from utils.http_client import new_finding


def run(target: str) -> list[dict]:
    findings = []

    # TODO: after manually confirming an XSS/SQLi/injection issue via
    # Burp Suite / OWASP ZAP / manual testing (see docs/methodology.md),
    # record it here using new_finding(), e.g.:
    #
    # findings.append(new_finding(
    #     finding_id="INPUT-001",
    #     title="Reflected XSS in search field",
    #     category="input_validation",
    #     severity="high",
    #     cvss_score=6.1,
    #     affected_component="/search?q=",
    #     description="...",
    #     reproduction_steps=["...", "..."],
    #     remediation="Sanitize/escape output and apply a Content-Security-Policy.",
    # ))

    return findings
