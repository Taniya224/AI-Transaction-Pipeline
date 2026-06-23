from app.services.gemini_service import generate_summary
import pandas as pd

def process_csv(file_path):

    df = pd.read_csv(file_path)

    raw_count = len(df)

    df = df.drop_duplicates()

    clean_count = len(df)

    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df = df.dropna(subset=["amount"])

    anomalies = []

    median_amount = df["amount"].median()

    for _, row in df.iterrows():

        reason = None

        if row["amount"] > median_amount * 3:
            reason = "Unusually High Transaction"

        elif (
            str(row["merchant"]).lower() in ["swiggy", "ola", "irctc"]
            and str(row["currency"]).upper() == "USD"
        ):
            reason = "Suspicious Currency Usage"

        if reason:
            anomalies.append({
                "txn_id": row["txn_id"],
                "merchant": row["merchant"],
                "amount": row["amount"],
                "reason": reason
            })

    summary = generate_summary({
        "raw_count": raw_count,
        "clean_count": clean_count,
        "anomaly_count": len(anomalies)
    })

    return {
        "raw_count": raw_count,
        "clean_count": clean_count,
        "columns": list(df.columns),
        "anomaly_count": len(anomalies),
        "anomalies": anomalies[:10],
        "ai_summary": summary
    }