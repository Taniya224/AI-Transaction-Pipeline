import json

from app.services.gemini_service import generate_summary
import pandas as pd


def process_csv(file_path):

    df = pd.read_csv(file_path)

    # Raw Count
    raw_count = len(df)

    # Remove Duplicates
    df = df.drop_duplicates()

    # Fill Missing Categories
    df["category"] = df["category"].fillna("Uncategorised")

    # Simple Category Classification
    for index, row in df.iterrows():

        if row["category"] == "Uncategorised":

            merchant = str(row["merchant"]).lower()

            if merchant in ["swiggy", "zomato"]:
                df.at[index, "category"] = "Food"

            elif merchant in ["ola", "uber"]:
                df.at[index, "category"] = "Transport"

            elif merchant in ["irctc"]:
                df.at[index, "category"] = "Travel"

            elif merchant in ["amazon", "flipkart"]:
                df.at[index, "category"] = "Shopping"

            elif merchant in ["jio recharge"]:
                df.at[index, "category"] = "Utilities"

            else:
                df.at[index, "category"] = "Other"

    # Normalize Status
    df["status"] = df["status"].astype(str).str.upper()

    # Normalize Currency
    df["currency"] = df["currency"].astype(str).str.upper()

    # Normalize Dates
    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    df["date"] = df["date"].dt.strftime("%Y-%m-%d")

    # Remove Currency Symbols
    df["amount"] = (
        df["amount"]
        .astype(str)
        .str.replace("$", "", regex=False)
    )

    # Convert Amount to Numeric
    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    )

    df = df.dropna(subset=["amount"])

    clean_count = len(df)

    # Account-wise Median Calculation
    account_medians = (
        df.groupby("account_id")["amount"]
        .median()
        .to_dict()
    )

    anomalies = []

    for _, row in df.iterrows():

        reason = None

        account_median = account_medians.get(
            row["account_id"],
            0
        )

        if account_median > 0 and row["amount"] > account_median * 3:
            reason = "Unusually High Transaction"

        elif (
            str(row["merchant"]).lower()
            in ["swiggy", "ola", "irctc"]
            and str(row["currency"]).upper() == "USD"
        ):
            reason = "Suspicious Currency Usage"

        if reason:
            anomalies.append({
                "txn_id": row["txn_id"],
                "merchant": row["merchant"],
                "amount": float(row["amount"]),
                "reason": reason
            })

    # Category Spend Breakdown
    category_spend = (
        df.groupby("category")["amount"]
        .sum()
        .round(2)
        .to_dict()
    )

    # Top Merchants
    top_merchants = (
        df.groupby("merchant")["amount"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .round(2)
        .to_dict()
    )

    # Risk Score
    risk_score = min(len(anomalies) * 10, 100)

    if risk_score >= 70:
        risk_level = "HIGH"
    elif risk_score >= 30:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    # AI Summary
    try:
        summary = generate_summary({
            "raw_count": raw_count,
            "clean_count": clean_count,
            "anomaly_count": len(anomalies),
            "category_spend": category_spend,
            "top_merchants": top_merchants,
            "risk_level": risk_level
        })

    except Exception as e:
        summary = f"AI Summary unavailable: {str(e)}"
    df = df.fillna("")
    df = df.replace([float("inf"), float("-inf")], 0)
    df = df.fillna("")
    return {
    "raw_count": raw_count,
    "clean_count": clean_count,
    "columns": list(df.columns),

    "anomaly_count": len(anomalies),
    "anomalies": anomalies[:10],

    "category_spend": category_spend,

    "top_merchants": top_merchants,

    "risk_score": risk_score,
    "risk_level": risk_level,

    "ai_summary": summary,

    "transactions": json.loads(
    df.fillna("")
      .to_json(orient="records")
    )
}