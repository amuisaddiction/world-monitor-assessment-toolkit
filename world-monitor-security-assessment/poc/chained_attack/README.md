# Chained Attack PoC — Narrative Template

Fill this in once you've confirmed real findings. This is your single
strongest demo artifact — prioritize it over covering every scope area shallowly.

## Attack path (example structure — replace with your actual chain)
1. **Step 1 — Initial foothold:** e.g. reflected/stored XSS in a user-facing
   field (`step1_xss.py`)
2. **Step 2 — Escalation:** e.g. stolen session token used to authenticate
   as the victim (`step2_token_extraction.py`)
3. **Step 3 — Impact:** e.g. IDOR on an authenticated endpoint used to
   access/modify another user's data (`step3_idor_exploit.py`)

## Why this matters
Explain in 2-3 sentences why the *combination* is worse than any single
finding — this is the narrative judges remember.

## Evidence
Screenshots/video for each step go in `../screenshots/`.
