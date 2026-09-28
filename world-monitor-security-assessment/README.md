# World Monitor Security Assessment

Authorized security assessment toolkit for the World Monitor app
(SIH problem statement — NTRO, Smart Automation).

## What this is
An automated scanner + AI-assisted triage + risk dashboard for assessing
the World Monitor app (github.com/koala73/worldmonitor), built and tested
against a **local instance only**.

## Quick start
1. Clone target app into `target/worldmonitor/`
2. Run it locally (see target/worldmonitor's own README for setup)
3. `cd scanner && pip install -r requirements.txt`
4. `python main.py --target http://localhost:<port>` → produces `findings.json`
5. `cd ../ai_triage && python generate_report.py` → produces report sections
6. Open `dashboard/index.html` to view the risk dashboard
7. Final report lives in `reports/security_assessment_report.md`

## Folder guide
- `docs/` — PRD, design doc, tech stack, architecture, security notes, methodology
- `scanner/` — automated vulnerability checks (core tool)
- `ai_triage/` — LLM-assisted writeup/remediation generation
- `dashboard/` — visual findings dashboard
- `poc/` — proof-of-concept demos, including one chained attack narrative
- `ci_integration/` — GitHub Action to run scans on every PR
- `reports/` — final deliverables (report + compliance mapping)

## Rules of engagement
Testing performed only against a locally-cloned, self-hosted instance.
No production systems, real user data, or destructive actions involved.
