# World Monitor Security Assessment Toolkit

A defensive, authorized security-assessment platform intended for controlled/local staging environments. Developed for SIH 2026 Problem Statement 26163.

## Architecture
- **Scanner/Engine:** Python modules for safe configuration, headers, and API analysis.
- **Backend:** FastAPI + SQLite/SQLAlchemy.
- **Dashboard:** Streamlit.
- **AI Triage:** Gemini integration with deterministic local fallback.
- **Mock Target:** Safe declarative configuration API for testing without exploitation.

## Local Setup
Ensure you have Python 3.10+ installed.
```bash
pip install -r requirements.txt
```

## Running the Application

### Single-Deployment Mode (Cloud / Render / Streamlit Cloud)
To run the complete platform (Test Target, API, and Dashboard) via a single command:
```bash
python run.py
```
This will start all internal services and bind the public dashboard to port `8501` (or `$PORT` if set). This is the recommended mode for 1-click cloud deployments.

### Multi-Terminal Mode (Development)
Run these commands in separate terminals:
1. `python test_target/app.py`
2. `uvicorn api.server:app --host 127.0.0.1 --port 8000`
3. `streamlit run dashboard/app.py`

### Docker Mode
If Docker is installed:
```bash
docker compose up -d --build
```

## Environment Variables
- `API_BASE_URL`: URL of the FastAPI backend (Default: `http://127.0.0.1:8000`)
- `TARGET_URL`: URL of the test target (Default: `http://127.0.0.1:8080`)
- `GEMINI_API_KEY`: (Optional) API key for Gemini report generation. If absent, the platform uses a deterministic local fallback.

## Demo Workflow
1. Navigate to the Streamlit Dashboard (default `http://localhost:8501`).
2. Go to **New Assessment** and click **START SECURITY ASSESSMENT**.
3. View **Findings** to see the generated security findings.
4. Go to **Reports** and generate the AI / Fallback Markdown report.
5. Go to **System Health** and click **RESET DEMO** to clear the database for the next judge.

## Security Limitations
- This platform operates strictly against the internal test target.
- It will safely reject public targets (e.g. `https://www.worldmonitor.app`).
- No exploits, destructive payloads, or credential attacks are performed.

## Troubleshooting
- **API Offline:** Ensure `API_BASE_URL` is set correctly for your environment. If running locally, check if `python run.py` completed successfully.
- **No Findings:** Ensure the test target is online at `TARGET_URL` (usually port `8080`). 
