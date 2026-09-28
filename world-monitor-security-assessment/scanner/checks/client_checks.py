"""
Client-side security checks: hardcoded secrets in JS bundles, CSP header.
"""
import re
from utils.http_client import get, new_finding

# Common patterns for accidentally-committed secrets in frontend bundles.
SECRET_PATTERNS = [
    (r"AIza[0-9A-Za-z\-_]{35}", "Google API key"),
    (r"sk_live_[0-9a-zA-Z]{24,}", "Stripe live secret key"),
    (r"AKIA[0-9A-Z]{16}", "AWS access key ID"),
]


def run(target: str) -> list[dict]:
    findings = []

    # --- Check 1: secrets in the main page / bundled JS ---------------------
    try:
        resp = get(target)
        for pattern, label in SECRET_PATTERNS:
            if re.search(pattern, resp.text):
                findings.append(new_finding(
                    finding_id="CLIENT-001",
                    title=f"Possible hardcoded {label} exposed client-side",
                    category="client",
                    severity="critical",
                    cvss_score=9.1,
                    affected_component=target,
                    description=f"A pattern matching a {label} was found in client-delivered content.",
                    reproduction_steps=[
                        f"Fetch {target} and view page source / bundled JS",
                        f"Search for the {label} pattern",
                    ],
                    remediation="Move secrets server-side; never ship API/secret keys in client bundles.",
                ))
    except Exception:
        pass

    # --- Check 2: missing Content-Security-Policy ----------------------------
    try:
        resp = get(target)
        if "content-security-policy" not in {k.lower() for k in resp.headers.keys()}:
            findings.append(new_finding(
                finding_id="CLIENT-002",
                title="Missing Content-Security-Policy header",
                category="client",
                severity="low",
                cvss_score=4.0,
                affected_component=target,
                description="No CSP header was found, reducing defense-in-depth against XSS.",
                reproduction_steps=[f"Inspect response headers for {target}"],
                remediation="Add a Content-Security-Policy header restricting script/style sources.",
            ))
    except Exception:
        pass

    return findings
