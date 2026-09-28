# Testing Methodology

1. **Recon** — clone repo, map routes/endpoints, identify auth flow, roles,
   and every input surface
2. **Baseline scan** — run `scanner/main.py` for automated coverage across
   all 7 scope areas
3. **Manual verification** — use Burp Suite/OWASP ZAP to manually confirm
   and deepen any automated finding (automated tools produce false positives —
   every finding in the final report must be manually reproduced)
4. **Chained attack construction** — pick the 2-3 most impactful findings and
   test whether they can be combined into a single realistic attack path
5. **AI-assisted triage** — run confirmed findings through `ai_triage/` for
   CVSS scoring rationale, business-impact writeups, and remediation drafts
   (human review required before including in the final report)
6. **Compliance mapping** — map each finding to OWASP Top 10 2025 and
   CERT-IN guidelines
7. **Reporting** — compile `reports/security_assessment_report.md`, individual
   `reports/findings/finding_XX.md` files, and the demo script/video

## Severity scoring
Use the official CVSS 3.1/4.0 calculator for every finding — don't eyeball
scores. Record the vector string alongside the numeric score for defensibility.
