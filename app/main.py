from fastapi import FastAPI
from app.api.jobs import router as jobs_router
from app.database.database import engine, Base

app = FastAPI(
    title="AI Transaction Processing Pipeline"
)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

app.include_router(jobs_router)

@app.get("/")
def home():
    return {
        "message": "API Running"
    }