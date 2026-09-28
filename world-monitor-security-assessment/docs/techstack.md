# Tech Stack

## Scanner (core tool)
- **Language:** Python 3.11+
- **HTTP:** `requests` (sync, simple) — swap for `httpx` if async needed
- **CLI:** `argparse`
- **Reporting:** `json` (stdlib) for findings.json

## AI Triage
- **LLM:** Claude or Gemini Pro API (per team preference — Gemini Pro is
  already in use for the rest of the project, so reuse the same API key/setup)
- **Prompting:** structured prompt templates in `ai_triage/prompts/`
- **Output:** Markdown findings + enriched findings.json

## Dashboard
- **Frontend:** plain HTML/CSS/JS (no framework) for zero-build-step demo
  reliability — optional upgrade to React if time allows
- **Charts:** simple inline SVG or Chart.js (CDN) for severity bar/heatmap

## CI Integration
- **GitHub Actions** — `ci_integration/.github/workflows/security-scan.yml`
- Runs scanner headlessly against a spun-up local instance in the CI runner

## Target app (under test)
- Whatever World Monitor itself uses (check its own repo) — scanner is
  black-box/API-level so it doesn't need to match the target's stack

## Dev tooling (recommended, not required)
- Burp Suite / OWASP ZAP for manual verification and fuzzing alongside the
  automated scanner
- `pytest` if you want unit tests around the check modules
