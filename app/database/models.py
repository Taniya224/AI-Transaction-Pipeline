from sqlalchemy import Date
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Float,
    Boolean,
    ForeignKey
)

from app.database.database import Base
from datetime import datetime


class Job(Base):

    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String)

    status = Column(String)

    results = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class Transaction(Base):

    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    job_id = Column(
        Integer,
        ForeignKey("jobs.id")
    )

    txn_id = Column(String)

    account_id = Column(String)

    date = Column(String)   # <-- ADD THIS

    merchant = Column(String)

    amount = Column(Float)

    currency = Column(String)

    status = Column(String)

    category = Column(String)

    is_anomaly = Column(
        Boolean,
        default=False
    )

    anomaly_reason = Column(Text)

    llm_category = Column(String)

    llm_raw_response = Column(Text)

    llm_failed = Column(
        Boolean,
        default=False
    )

    anomaly_reason = Column(Text)

    llm_category = Column(String)

    llm_raw_response = Column(Text)

    llm_failed = Column(
        Boolean,
        default=False
    )


class JobSummary(Base):

    __tablename__ = "job_summaries"

    id = Column(Integer, primary_key=True, index=True)

    job_id = Column(
        Integer,
        ForeignKey("jobs.id")
    )

    total_spend_inr = Column(Float)

    total_spend_usd = Column(Float)

    top_merchants = Column(Text)

    anomaly_count = Column(Integer)

    narrative = Column(Text)

    risk_level = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )