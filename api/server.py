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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
