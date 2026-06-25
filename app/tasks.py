from app.database.models import Transaction
from app.services.csv_processor import process_csv
from app.database.database import SessionLocal
from app.database.models import Job, JobSummary
import json


def process_job(job_id, filepath):

    db = SessionLocal()

    job = db.query(Job).filter(
        Job.id == job_id
    ).first()

    if not job:
        db.close()
        return

    try:

        job.status = "processing"
        db.commit()

        analysis = process_csv(filepath)

        job.status = "completed"
        job.results = json.dumps(analysis)

        category_spend = analysis.get(
            "category_spend",
            {}
        )

        total_spend_inr = sum(
            float(v)
            for v in category_spend.values()
        )

        # Save transactions
        for txn in analysis.get("transactions", []):

            transaction = Transaction(
                job_id=job.id,
                txn_id=str(txn.get("txn_id")),
                account_id=str(txn.get("account_id")),
                date=txn.get("date"),
                merchant=txn.get("merchant"),
                amount=float(txn.get("amount", 0)),
                currency=txn.get("currency"),
                status=txn.get("status"),
                category=txn.get("category"),
                is_anomaly=False,
                anomaly_reason=None
            )

            db.add(transaction)

        db.commit()

        # Save summary
        summary = JobSummary(
            job_id=job.id,
            total_spend_inr=total_spend_inr,
            total_spend_usd=0,
            top_merchants=json.dumps(
                analysis.get(
                    "top_merchants",
                    {}
                )
            ),
            anomaly_count=analysis.get(
                "anomaly_count",
                0
            ),
            narrative=json.dumps(
                analysis.get(
                    "ai_summary",
                    {}
                )
            ),
            risk_level=analysis.get(
                "risk_level",
                "LOW"
            )
        )

        db.add(summary)
        db.commit()

    except Exception as e:

        db.rollback()

        job = db.query(Job).filter(
            Job.id == job_id
        ).first()

        if job:
            job.status = "failed"
            job.results = json.dumps({
                "error": str(e)
            })
            db.commit()

        raise

    finally:
        db.close()