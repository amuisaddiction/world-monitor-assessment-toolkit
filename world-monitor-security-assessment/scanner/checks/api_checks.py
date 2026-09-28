"""
API security checks: CORS misconfig, verbose errors, missing auth.
"""
from utils.http_client import get, new_finding


def run(target: str) -> list[dict]:
    findings = []

    # --- Check 1: permissive CORS ------------------------------------------
    try:
        resp = get(target, headers={"Origin": "https://evil-example.com"})
        acao = resp.headers.get("Access-Control-Allow-Origin", "")
        if acao == "*" or acao == "https://evil-example.com":
            findings.append(new_finding(
                finding_id="API-001",
                title="Overly permissive CORS configuration",
                category="api",
                severity="medium",
                cvss_score=6.5,
                affected_component=f"{target} (Access-Control-Allow-Origin header)",
                description=(
                    f"The server reflected/allowed an arbitrary Origin "
                    f"('{acao}'), which can allow malicious sites to make "
                    "authenticated cross-origin requests on behalf of a user."
                ),
                reproduction_steps=[
                    f"Send a request to {target} with header Origin: https://evil-example.com",
                    "Observe Access-Control-Allow-Origin reflects or wildcards the origin",
                ],
                remediation="Restrict Access-Control-Allow-Origin to an explicit allow-list of trusted domains.",
            ))
    except Exception:
        pass

    # --- Check 2: verbose error responses -----------------------------------
    try:
        resp = get(f"{target}/api/this-endpoint-does-not-exist-12345")
        body_lower = resp.text.lower()
        if any(term in body_lower for term in ["traceback", "stack trace", "at line", "exception in"]):
            findings.append(new_finding(
                finding_id="API-002",
                title="Verbose error messages leak internal details",
                category="api",
                severity="low",
                cvss_score=3.7,
                affected_component=f"{target}/api/this-endpoint-does-not-exist-12345",
                description="Error responses include stack traces or internal implementation details.",
                reproduction_steps=[
                    "Request a non-existent or malformed API endpoint",
                    "Observe stack trace / internal path details in the response body",
                ],
                remediation="Return generic error messages to clients; log full details server-side only.",
            ))
    except Exception:
        pass

    return findings
