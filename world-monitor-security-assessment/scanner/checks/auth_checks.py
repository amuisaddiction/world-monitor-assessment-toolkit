"""
Authentication & session management checks.

Run only against a LOCAL, self-hosted instance you control.
"""
from utils.http_client import get, post, new_finding


def run(target: str) -> list[dict]:
    findings = []

    # --- Check 1: login rate limiting -------------------------------------
    # TODO: point this at your target's actual login endpoint once you've
    # mapped it during recon (docs/methodology.md step 1).
    login_url = f"{target}/api/auth/login"
    try:
        responses = [
            post(login_url, json_body={"email": "test@example.com", "password": "wrong"})
            for _ in range(10)
        ]
        status_codes = [r.status_code for r in responses]
        if status_codes.count(401) == len(status_codes) and 429 not in status_codes:
            findings.append(new_finding(
                finding_id="AUTH-001",
                title="No rate limiting on login endpoint",
                category="auth",
                severity="medium",
                cvss_score=5.3,
                affected_component=login_url,
                description=(
                    "Sending repeated failed login attempts did not trigger any "
                    "rate limiting or account lockout (no 429 response observed "
                    "across 10 rapid attempts)."
                ),
                reproduction_steps=[
                    f"Send 10+ rapid POST requests to {login_url} with an invalid password",
                    "Observe that all requests return 401 with no throttling",
                ],
                remediation=(
                    "Add rate limiting (e.g. per-IP and per-account) and/or "
                    "progressive delays or CAPTCHA after N failed attempts."
                ),
            ))
    except Exception:
        pass  # target may not be reachable yet — handled by main.py's error wrapper

    # --- Check 2: session cookie flags -------------------------------------
    try:
        resp = get(target)
        set_cookie = resp.headers.get("Set-Cookie", "")
        if set_cookie and ("HttpOnly" not in set_cookie or "Secure" not in set_cookie):
            findings.append(new_finding(
                finding_id="AUTH-002",
                title="Session cookie missing security flags",
                category="auth",
                severity="medium",
                cvss_score=5.9,
                affected_component=f"{target} (Set-Cookie header)",
                description=(
                    "The session cookie is missing the HttpOnly and/or Secure "
                    "flag, increasing exposure to XSS-based session theft or "
                    "transmission over unencrypted connections."
                ),
                reproduction_steps=[
                    f"Inspect the Set-Cookie header returned by {target}",
                    "Confirm HttpOnly and Secure flags are absent",
                ],
                remediation="Set HttpOnly, Secure, and SameSite=Strict/Lax on all session cookies.",
            ))
    except Exception:
        pass

    return findings
