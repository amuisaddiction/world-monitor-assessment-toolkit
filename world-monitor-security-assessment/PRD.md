# PRD — World Monitor Security Assessment Toolkit

## 1. Problem Statement
NTRO (SIH, Smart Automation) requires an authorized security assessment of the
World Monitor web/mobile platform (worldmonitor.app), covering authentication,
authorization, input validation, API security, client-side security, secure
communication, and data storage — with documented, reproducible PoCs and
remediation guidance.

## 2. Objective
Build a reusable, automated security assessment toolkit — not a one-off manual
audit — that:
- Scans a local/controlled instance of World Monitor for vulnerabilities across
  all required scope areas
- Uses AI-assisted triage to generate CVSS scoring, business-impact writeups,
  and remediation suggestions
- Visualizes findings on a risk dashboard
- Can be wired into CI (GitHub Actions) to run on every PR ("shift-left security")
- Produces a final compliance-mapped report (OWASP Top 10 / CERT-IN) as the
  official deliverable

## 3. Target Users
- Immediate: hackathon judges (NTRO) evaluating the submission
- Real-world: dev teams who want a lightweight, repeatable security check
  before every release

## 4. Scope (from problem statement)
| Area | In scope |
|---|---|
| Auth & session management | Yes |
| Authorization & access control | Yes |
| Input validation & data handling | Yes |
| API security | Yes |
| Client-side security controls | Yes |
| Secure communication | Yes |
| Data storage & privacy | Yes |

## 5. Out of Scope
- Testing against the live production worldmonitor.app
- Denial-of-service or destructive testing
- Anything outside the cloned open-source repo running locally

## 6. Success Criteria
- At least one valid, evidenced vulnerability per scope area (target)
- Each finding has: title, description, affected component, CVSS score,
  reproduction steps, PoC, business impact, remediation
- Working scanner tool producing machine-readable findings (JSON)
- Dashboard visualizing severity/attack surface
- Final report mapped to a recognized compliance framework

## 7. Milestones
1. Recon + local environment setup
2. Scanner core + per-area check modules
3. AI triage pipeline (findings.json → written report sections)
4. Dashboard (severity heatmap, attack surface map)
5. One chained-attack PoC narrative + video
6. CI integration (GitHub Action)
7. Final report + CERT-IN/OWASP mapping + demo script

## 8. Risks
- Time: 7 scope areas is broad — prioritize 2-3 deep findings + 1 chained
  attack over shallow coverage of everything
- Legal/ethical: only ever test the locally-cloned instance, never the
  production app or real user data
