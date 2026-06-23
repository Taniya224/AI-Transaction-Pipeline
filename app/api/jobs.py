from fastapi import APIRouter, UploadFile, File
from app.services.csv_processor import process_csv
from app.database.database import SessionLocal
from app.database.models import Job

import json
import os

router = APIRouter()

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/jobs/upload")
async def upload_file(file: UploadFile = File(...)):

    filepath = os.path.join(UPLOAD_DIR, file.filename)

    with open(filepath, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    analysis = process_csv(filepath)

    db = SessionLocal()

    job = Job(
        filename=file.filename,
        status="completed",
        results=json.dumps(analysis)
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    db.close()

    return {
        "job_id": job.id,
        "status": job.status,
        "message": "Job created successfully"
    }


@router.get("/jobs")
def get_jobs():

    db = SessionLocal()

    jobs = db.query(Job).all()

    result = []

    for job in jobs:
        result.append({
            "id": job.id,
            "filename": job.filename,
            "status": job.status
        })

    db.close()

    return result


@router.get("/jobs/{job_id}/status")
def get_status(job_id: int):

    db = SessionLocal()

    job = db.query(Job).filter(Job.id == job_id).first()

    db.close()

    if not job:
        return {"error": "Job not found"}

    return {
        "job_id": job.id,
        "status": job.status
    }


@router.get("/jobs/{job_id}/results")
def get_results(job_id: int):

    db = SessionLocal()

    job = db.query(Job).filter(Job.id == job_id).first()

    db.close()

    if not job:
        return {"error": "Job not found"}

    return {
        "job_id": job.id,
        "status": job.status,
        "results": json.loads(job.results)
    }