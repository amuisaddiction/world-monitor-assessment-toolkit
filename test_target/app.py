from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json
import os
import uvicorn

app = FastAPI(title="Mock World Monitor Target", description="Safe local target for SIH demonstration")

PROFILE_PATH = os.path.join(os.path.dirname(__file__), "security_profile.json")

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "test_target"}

@app.get("/api/status")
def api_status():
    return {"status": "operational", "version": "1.0.0"}

@app.get("/api/config")
def get_security_profile():
    try:
        with open(PROFILE_PATH, "r") as f:
            data = json.load(f)
        return JSONResponse(content=data)
    except FileNotFoundError:
        return JSONResponse(status_code=500, content={"error": "Security profile not found"})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
