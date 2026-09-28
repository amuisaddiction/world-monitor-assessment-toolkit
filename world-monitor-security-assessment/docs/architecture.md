# Architecture

## System diagram (textual)

```
                     +--------------------------+
                     |  Target: World Monitor    |
                     |   (local instance)        |
                     +-------------+--------------+
                                   | HTTP requests
                                   v
   +---------------------------------------------------+
   |                     scanner/                       |
   |  checks/auth_checks.py                              |
   |  checks/authz_checks.py                             |
   |  checks/input_validation_checks.py                  |
   |  checks/api_checks.py                                |
   |  checks/client_checks.py                             |
   |  checks/transport_checks.py                          |
   |              |                                       |
   |              v                                       |
   |           main.py  -----------> findings.json         |
   +---------------------------------------------------+
                                   |
                   +---------------+----------------+
                   v                                 v
        +----------------------+         +--------------------------+
        |   ai_triage/          |         |    dashboard/              |
        | generate_report.py    |         | index.html + data/        |
        | (LLM enrichment)      |         | findings.json             |
        +-----------+------------+         +--------------------------+
                    v
        +--------------------------+
        |        reports/           |
        | security_assessment_      |
        | report.md, findings/*.md, |
        | cert_in_compliance_*.md   |
        +--------------------------+

        +--------------------------+
        |   ci_integration/          |
        | GitHub Action runs          |
        | scanner/main.py on PRs     |
        +--------------------------+
```

## Design principles
- **Black-box first:** scanner talks to the app only over HTTP, same as a
  real attacker would — no special access needed, easy to demo
- **Single source of truth:** `findings.json` is the contract every other
  module reads from — keeps modules independently testable
- **Fail loud, not silent:** any check that errors out logs it as an
  `info`-severity finding rather than crashing the whole scan
