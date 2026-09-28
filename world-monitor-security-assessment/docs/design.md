# Design Document

## 1. Overview
The toolkit is composed of four independent, loosely-coupled modules that
communicate through a shared `findings.json` contract:

```
scanner  --produces-->  findings.json  --consumed by-->  ai_triage, dashboard
```

This lets each module be built/demoed independently and keeps the AI and
visualization layers swappable without touching the scanning logic.

## 2. findings.json schema
```json
{
  "scan_id": "string",
  "target": "string (url)",
  "timestamp": "ISO8601",
  "findings": [
    {
      "id": "F-001",
      "title": "string",
      "category": "auth | authz | input_validation | api | client | transport | storage",
      "severity": "critical | high | medium | low | info",
      "cvss_score": 0.0,
      "affected_component": "string (route/file)",
      "description": "string",
      "reproduction_steps": ["string"],
      "evidence": "path to screenshot/log",
      "remediation": "string",
      "status": "open | fixed | accepted_risk"
    }
  ]
}
```

## 3. Module responsibilities

**scanner/**
- Runs each `checks/*.py` module against the target
- Each check returns a list of finding dicts matching the schema above
- `main.py` aggregates all check results into one `findings.json`

**ai_triage/**
- Reads `findings.json`
- For findings missing a human-quality description/remediation, calls the
  LLM with a structured prompt (see `prompts/finding_writeup_prompt.txt`)
- Writes enriched output back to `findings.json` and generates
  `reports/findings/finding_XX.md` per finding

**dashboard/**
- Static HTML/JS reading `dashboard/data/findings.json`
- Renders: severity distribution (bar/heatmap), attack-surface map (list of
  endpoints color-coded by max severity found), findings table

**ci_integration/**
- GitHub Action triggers `scanner/main.py` on pull_request
- Fails the build (or comments on PR) if new critical/high findings appear

## 4. Data flow diagram
See `architecture.md` for the full system diagram.

## 5. UX notes (dashboard)
- Single page, no build step required (plain HTML/CSS/JS) so it can be
  opened directly or hosted as a static artifact
- Severity color convention: critical=red, high=orange, medium=yellow,
  low=blue, info=grey
