def generate_summary(data):
    return {
        "summary": f"Processed {data['clean_count']} clean records from {data['raw_count']} uploaded records.",
        "risk_level": "Medium" if data["anomaly_count"] > 0 else "Low",
        "anomaly_count": data["anomaly_count"]
    }