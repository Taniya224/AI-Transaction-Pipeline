from fastapi import FastAPI

from app.api.jobs import router as jobs_router

from app.database.database import engine
from app.database.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Transaction Processing Pipeline"
)

app.include_router(jobs_router)

@app.get("/")
def home():
    return {
        "message": "API Running"
    }