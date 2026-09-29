from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.database import engine, Base
from api.routes import health, scans, findings, reports

Base.metadata.create_all(bind=engine)

app = FastAPI(title="World Monitor Security API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(scans.router)
app.include_router(findings.router)
app.include_router(reports.router)

@app.post("/api/reset")
def reset_demo():
    # Safely clear the database for a clean demonstration state
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    return {"status": "success", "message": "Database reset"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
