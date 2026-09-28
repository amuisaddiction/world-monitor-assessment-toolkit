"""
Thin wrapper around `requests` for the scanner's check modules.

Keeping this centralized makes it easy to add: timeouts, consistent headers,
retry logic, and a place to plug in auth tokens for authenticated checks.
"""
import requests

DEFAULT_TIMEOUT = 10


def get(url: str, headers: dict | None = None, **kwargs) -> requests.Response:
    return requests.get(url, headers=headers, timeout=DEFAULT_TIMEOUT, **kwargs)


def post(url: str, json_body: dict | None = None, headers: dict | None = None, **kwargs) -> requests.Response:
    return requests.post(url, json=json_body, headers=headers, timeout=DEFAULT_TIMEOUT, **kwargs)


def new_finding(
    finding_id: str,
    title: str,
    category: str,
    severity: str,
    cvss_score: float,
    affected_component: str,
    description: str,
    reproduction_steps: list[str],
    remediation: str,
    evidence: str = "",
) -> dict:
    """Helper to build a finding dict matching the schema in docs/design.md."""
    return {
        "id": finding_id,
        "title": title,
        "category": category,
        "severity": severity,
        "cvss_score": cvss_score,
        "affected_component": affected_component,
        "description": description,
        "reproduction_steps": reproduction_steps,
        "evidence": evidence,
        "remediation": remediation,
        "status": "open",
    }
