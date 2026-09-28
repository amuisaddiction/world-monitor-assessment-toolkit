"""
Authorization & access control checks (IDOR, privilege escalation).

TODO: fill in real endpoint patterns discovered during recon
(docs/methodology.md step 1) — e.g. GET /api/reports/{id}.
"""
from utils.http_client import get, new_finding


def run(target: str) -> list[dict]:
    findings = []

    # --- Check: IDOR probe on a numeric resource ID -------------------------
    # Adjust `resource_path` to a real endpoint from your recon notes.
    resource_path = "/api/reports/1"
    try:
        resp = get(f"{target}{resource_path}")
        # A 200 with no auth header at all is a strong signal of missing
        # authorization on a resource that should require ownership/role checks.
        if resp.status_code == 200:
            findings.append(new_finding(
                finding_id="AUTHZ-001",
                title="Possible IDOR / missing authorization check",
                category="authz",
                severity="high",
                cvss_score=7.5,
                affected_component=resource_path,
                description=(
                    f"Requesting {resource_path} without any authentication "
                    "returned HTTP 200, suggesting the endpoint does not "
                    "enforce ownership or role checks."
                ),
                reproduction_steps=[
                    f"GET {target}{resource_path} with no Authorization header",
                    "Observe HTTP 200 and inspect returned data for another user's resource",
                ],
                remediation=(
                    "Enforce server-side ownership/role checks on every "
                    "resource-by-ID endpoint; never trust client-supplied IDs alone."
                ),
            ))
    except Exception:
        pass

    return findings
