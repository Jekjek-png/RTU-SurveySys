from pathlib import Path
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import csv

router = APIRouter()

DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "Survey_response.csv"

class SurveyResponse(BaseModel):
    service_id: str
    service_availed: str
    respondent_name: str
    date_of_visit: str
    age_bracket: str
    gender: str
    category_of_respondent: str
    cc1: str
    cc2: str
    cc3: str
    service_satisfaction: int
    service_time: int
    service_requirements: int
    service_steps: int
    service_transaction: int
    service_fee: str
    service_fair: int
    service_courtesy: int
    service_request: int
    comments_suggestions: str
    attending_employee: str
    comments_suggestions_for_employee: str

CSV_HEADERS = [
    "service_id",
    "service_Availed",
    "respondent_name",
    "date_of_visit",
    "age_bracket",
    "gender",
    "category_of_respondent",
    "cc1",
    "cc2",
    "cc3",
    "service_satisfaction(1-5)",
    "service_time(1-5)",
    "service_requirements(1-5)",
    "service_steps(1-5)",
    "service_transaction(1-5)",
    "service_fee(1-5 or N/A)",
    "service_fair(1-5)",
    "service_courtesy(1-5)",
    "service_request(1-5)",
    "comments_suggestions",
    "attending_employee",
    "comments_suggestions_for_employee",
]

@router.post("/Submit survey response", response_model=SurveyResponse)
def post_response(response: SurveyResponse):
    try:
        file_exists = DATA_FILE.exists()

        with DATA_FILE.open("a", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=CSV_HEADERS)

            writer.writerow({
                "service_id": response.service_id,
                "service_Availed": response.service_availed,
                "respondent_name": response.respondent_name,
                "date_of_visit": response.date_of_visit,
                "age_bracket": response.age_bracket,
                "gender": response.gender,
                "category_of_respondent": response.category_of_respondent,
                "cc1": response.cc1,
                "cc2": response.cc2,
                "cc3": response.cc3,
                "service_satisfaction(1-5)": response.service_satisfaction,
                "service_time(1-5)": response.service_time,
                "service_requirements(1-5)": response.service_requirements,
                "service_steps(1-5)": response.service_steps,
                "service_transaction(1-5)": response.service_transaction,
                "service_fee(1-5 or N/A)": response.service_fee,
                "service_fair(1-5)": response.service_fair,
                "service_courtesy(1-5)": response.service_courtesy,
                "service_request(1-5)": response.service_request,
                "comments_suggestions": response.comments_suggestions,
                "attending_employee": response.attending_employee,
                "comments_suggestions_for_employee": response.comments_suggestions_for_employee,
            })

        return response
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Could not save survey response: {exc}")
