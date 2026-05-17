from pathlib import Path
from fastapi import APIRouter, HTTPException
import csv

router = APIRouter()

SURVEY_FILE = Path(__file__).resolve().parents[2] / "data" / "Survey_response.csv"

@router.get("/get_service_responses/{service_id}")
def get_responses_by_service(service_id: str):
    if not SURVEY_FILE.exists():
        raise HTTPException(status_code=500, detail="Survey response data file not found")


    matching_responses = []

    with SURVEY_FILE.open(mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:

            if row.get("service_id", "").strip() == service_id:
                matching_responses.append(row)
    
    if len(matching_responses) == 0:
        raise HTTPException(status_code=404, detail=f"No survey responses found yet for Service/Department")

    return {
        "status": "success",
        "total_responses": len(matching_responses),
        "data": matching_responses
    }