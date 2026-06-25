from app.tasks import process_job
from fastapi import APIRouter, UploadFile, File
from app.database.database import SessionLocal
from app.database.models import Job, JobSummary, Transaction
import json
import os
from redis import Redis
from rq import Queue

router = APIRouter()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

redis_conn = Redis(
    host="redis",
    port=6379
)

queue = Queue(connection=redis_conn)


@router.post("/jobs/upload")
async def upload_file(file: UploadFile = File(...)):

    db = SessionLocal()

    job = Job(
        filename=file.filename,
        status="pending"
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    filepath = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(filepath, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    try:
        queue.enqueue(
    process_job,
    job.id,
    filepath
)

    except Exception as e:

        job.status = "failed"

        job.results = json.dumps({
            "error": str(e)
        })

        db.commit()

    response = {
        "job_id": job.id,
        "status": job.status,
        "message": "Job queued successfully"
    }

    db.close()

    return response


@router.get("/jobs/{job_id}/status")
def get_status(job_id: int):

    db = SessionLocal()

    job = db.query(Job).filter(
        Job.id == job_id
    ).first()

    if not job:
        db.close()
        return {"error": "Job not found"}

    summary = None

    if job.results:

        data = json.loads(job.results)

        summary = {
            "anomaly_count": data.get("anomaly_count"),
            "categories": list(
                data.get("category_spend", {}).keys()
            ),
            "risk_level": data.get("risk_level")
        }

    result = {
        "job_id": job.id,
        "filename": job.filename,
        "status": job.status,
        "created_at": str(job.created_at),
        "summary": summary
    }

    db.close()

    return result


@router.get("/jobs/{job_id}/results")
def get_results(job_id: int):

    db = SessionLocal()

    job = db.query(Job).filter(
        Job.id == job_id
    ).first()

    if not job:
        db.close()

        return {
            "error": "Job not found"
        }

    result = {
        "job_id": job.id,
        "filename": job.filename,
        "status": job.status,
        "created_at": str(job.created_at),
        "results": json.loads(
            job.results
        ) if job.results else {}
    }

    db.close()

    return result


@router.get("/jobs")
def get_all_jobs(status: str = None):

    db = SessionLocal()

    query = db.query(Job)

    if status:
        query = query.filter(
            Job.status == status
        )

    jobs = query.all()

    result = [
        {
            "id": job.id,
            "filename": job.filename,
            "status": job.status,
            "created_at": str(job.created_at)
        }
        for job in jobs
    ]

    db.close()

    return result


@router.get("/jobs/{job_id}/summary")
def get_job_summary(job_id: int):

    db = SessionLocal()

    summary = db.query(JobSummary).filter(
        JobSummary.job_id == job_id
    ).first()

    if not summary:
        db.close()

        return {
            "error": "Summary not found"
        }

    result = {
        "job_id": summary.job_id,
        "total_spend_inr": summary.total_spend_inr,
        "total_spend_usd": summary.total_spend_usd,
        "top_merchants": json.loads(
            summary.top_merchants
        ),
        "anomaly_count": summary.anomaly_count,
        "risk_level": summary.risk_level,
        "narrative": summary.narrative
    }

    db.close()

    return result


@router.get("/jobs/{job_id}/transactions")
def get_transactions(job_id: int):

    db = SessionLocal()

    transactions = db.query(
        Transaction
    ).filter(
        Transaction.job_id == job_id
    ).all()

    result = [
        {
            "txn_id": t.txn_id,
            "account_id": t.account_id,
            "merchant": t.merchant,
            "amount": t.amount,
            "currency": t.currency,
            "status": t.status,
            "category": t.category,
            "is_anomaly": t.is_anomaly,
            "anomaly_reason": t.anomaly_reason
        }
        for t in transactions
    ]

    db.close()

    return result