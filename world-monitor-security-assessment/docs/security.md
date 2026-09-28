# Security Notes & Rules of Engagement

## Testing boundaries
- All testing is performed against a **locally-cloned, self-hosted instance**
  of World Monitor (from github.com/koala73/worldmonitor) — never against the
  live production worldmonitor.app
- No real user accounts, real user data, or third-party systems are touched
- No denial-of-service, data-destruction, or persistence/backdoor techniques
  are used — PoCs are limited to demonstrating that a vulnerability exists

## Handling of findings
- Findings are stored locally in `findings.json` and `reports/` — not
  published or shared outside the team/submission until remediation guidance
  is included
- Any credentials, tokens, or secrets discovered during testing are treated
  as sensitive: redact them in screenshots/reports (e.g. `sk-***redacted***`)

## Secure-by-default practices applied to this project itself
- `.env.example` is committed, `.env` (real keys) is gitignored
- LLM API keys used in `ai_triage/` are read from environment variables only,
  never hardcoded
- The scanner defaults to a `--target` flag pointing at `localhost` — it does
  not have a hardcoded production URL to reduce accidental misuse

## Responsible disclosure note
This assessment is conducted under the explicit authorization of the SIH/NTRO
problem statement, scoped to the open-source repository. If findings are
later reported upstream to the real World Monitor maintainers, follow
standard responsible disclosure practice (private report first, reasonable
fix window before any public writeup).
