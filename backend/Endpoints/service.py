from pathlib import Path
from fastapi import FastAPI, HTTPException
import csv

app = FastAPI()

DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "Services.csv"
    
@app.get("/services")
def get_services():
    if not DATA_FILE.exists():
        raise HTTPException(
            status_code=500,
            detail=f"Services data file not found: {DATA_FILE}"
        )

    services = []
    with DATA_FILE.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            services.append({
                "service_id": row.get("service_id", "").strip(),
                "service_name": row.get("service_name", "").strip(),
            })

    return {"services": services}
