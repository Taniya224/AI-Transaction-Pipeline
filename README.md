# AI Transaction Processing Pipeline

## Overview

A backend system that processes transaction CSV files asynchronously using Redis and RQ workers. The system cleans transaction data, detects anomalies, calculates risk scores, generates AI-powered summaries, and stores results in PostgreSQL.

## Tech Stack

* FastAPI
* PostgreSQL
* SQLAlchemy
* Redis
* RQ
* Pandas
* Docker
* Gemini API

## Architecture

Client → FastAPI → Redis Queue → RQ Worker → CSV Processing → PostgreSQL

## Setup Instructions

### Clone Repository

```bash
git clone https://github.com/Taniya224/AI-Transaction-Pipeline
cd ai-transaction-pipeline/app/api
```

### Start Services

```bash
docker compose up --build
```

### API Documentation

```text
http://localhost:8000/docs
```

## Example API Requests

### Upload CSV

```bash
curl -X POST "http://localhost:8000/jobs/upload" \
-F "file=@transactions.csv"
```

### Get All Jobs

```bash
curl http://localhost:8000/jobs
```

### Check Job Status

```bash
curl http://localhost:8000/jobs/1/status
```

### Get Results

```bash
curl http://localhost:8000/jobs/1/results
```

### Get Summary

```bash
curl http://localhost:8000/jobs/1/summary
```

### Get Transactions

```bash
curl http://localhost:8000/jobs/1/transactions
```

## Features

* Asynchronous CSV processing
* Transaction categorization
* Anomaly detection
* Risk scoring
* AI-generated summaries
* PostgreSQL persistence
* Dockerized deployment

