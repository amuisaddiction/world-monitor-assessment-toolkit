# World Monitor Security Assessment Toolkit

A defensive, authorized security-assessment platform intended for controlled/local staging environments. Developed for SIH 2026 Problem Statement 26163.

## Architecture
- **Scanner/Engine:** Python modules for safe configuration, headers, and API analysis.
- **Backend:** FastAPI + SQLite/SQLAlchemy.
- **Dashboard:** Streamlit.
- **AI Triage:** Gemini integration with deterministic local fallback.
- **Mock Target:** Safe declarative configuration API for testing without exploitation.

## Local Workflow (Windows PowerShell)
Run these commands in separate terminals:
1. `python test_target/app.py`
2. `uvicorn api.server:app --host 127.0.0.1 --port 8000`
3. `streamlit run dashboard/app.py`

## Docker Workflow
```bash
docker compose up -d --build
```
Access the dashboard at `http://localhost:8501`.

## Testing
Run `pytest -q` to execute the full test suite.
