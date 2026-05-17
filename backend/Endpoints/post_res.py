from pathlib import Path
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, field_validator
import csv
from datetime import datetime

router = APIRouter()

DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "Survey_response.csv"

class SuccessResponse(BaseModel):
    Message: str

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

    @field_validator("service_satisfaction", "service_time", "service_requirements", "service_steps", "service_transaction", "service_fair", "service_courtesy", "service_request")
    @classmethod
    def validate_rating(cls, value):
        if not (1 <= value <= 5):
            raise ValueError("Rating must be between 1 and 5.")
        return value
    
    @field_validator("service_fee")
    @classmethod
    def validate_service_fee(cls, value):
            if value != "N/A" and not value.isdigit():
                raise ValueError("Service fee must be an integer between 1 and 5 or 'N/A'.")
            if value.isdigit() and not (1 <= int(value) <= 5):
                raise ValueError("Service fee rating must be between 1 and 5 or 'N/A'.")
            return value
    
    @field_validator("service_id")
    @classmethod
    def validate_service_id(cls, value):
        valid_service_id = [
            "SV001",
            "SV002",
            "SV003"
        ]
        if value.strip() == "":
            raise ValueError("Service ID cannot be empty.")
        if value not in valid_service_id:
            raise ValueError("Service ID must be one of SV001, SV002, SV003.")
        return value
    
    @field_validator("respondent_name")
    @classmethod
    def validate_respondent_name(cls, value):
        if value.strip() == "":
            raise ValueError("Respondent name cannot be empty.")
        if len(value) > 60:
            raise ValueError("Respondent name cannot exceed 60 characters.")
        return value
    
    @field_validator("service_availed")
    @classmethod
    def validate_service_availed(cls, value):

        if value.strip() == "":
            raise ValueError("Service availed cannot be empty.")
        if len(value) > 70:
            raise ValueError("Service availed cannot exceed 70 characters")
        return value
    
    @field_validator("date_of_visit")
    @classmethod
    def validate_date_of_visit(cls, value):
        try:
            datetime.strptime(value, "%d/%m/%Y")
        except ValueError:
             raise ValueError("Date must be in DD/MM/YYYY format.")
        return value
    
    @field_validator("age_bracket")
    @classmethod
    def validate_age_bracket(cls, value):
        valid_age_bracket = [
            "16-Below",
            "17-20",
            "21-25",
            "26 and up"
            ]
        if value.strip() == "":
            raise ValueError("Age bracket must not be empty.")
        if value not in valid_age_bracket:
            raise ValueError("Age bracket must be one of: '16-Below', '17-20', '21-25', '26 and up'.")
        return value
    
    @field_validator("gender")
    @classmethod
    def validate_gender(cls, value):
        valid_gender = ["Male", "Female"]
        if value.strip() =="":
            raise ValueError("Gender must not be empty.")
        if value not in valid_gender:
            raise ValueError("Gender must be Male or Female only.")
        return value
    
    @field_validator("category_of_respondent")
    @classmethod
    def validate_category_of_respondent(cls, value):
        valid_res_category = [
            "Student", 
            "Alumni",
            "Employee", 
            "Visitor", 
            "Parent/s", 
            "Supplier", 
            "LGU / Government Agency Respresentative",
            "Industry Practitioners",
            "Administrative Employee", 
            "Faculty", 
            "Other"
            ]
        if value.strip() == "":
            raise ValueError("Category of respondent must not be empty.")
        if value not in valid_res_category:
            raise ValueError("Category of respondent must be in one of the choices.")
        return value
    
    @field_validator("comments_suggestions", "comments_suggestions_for_employee")
    @classmethod
    def validate_comments_suggestions(cls, value):
        if len(value) > 150:
            raise ValueError("Comments and suggestions cannot exceed 150 characters.")
        return value
    
    @field_validator("attending_employee")
    @classmethod
    def validate_attending_employee(cls, value):
        if value.strip() == "":
            raise ValueError("Attending Employee name cannot be empty")
        if len(value) > 60:
            raise ValueError("Attending Employee name cannot exceed 60 characters.")
        return value 
    
    @field_validator("cc1")
    @classmethod
    def validate_cc1(cls, value):
        valid_cc1_ans = [
            "I know what a CC is and I saw this office's CC",
            "I know what a CC is but I did not see this office's CC", 
            "I learned of the CC only when I saw this office's CC", 
            "I do not know what a CC is and did not see one in this office" 
            ]
        if value.strip() == "":
            raise ValueError("This field cannot be empty.")
        if value not in valid_cc1_ans:
            raise ValueError ("Answer must be in one of the choices.")
        return value
    
    @field_validator("cc2")
    @classmethod
    def validate_cc2(cls, value):
        valid_cc2_ans = [
            "Easy to see", 
            "Somewhat easy to see",
            "Difficult to see",
            "Not visible at all",
            "N/A"
            ]
        if value.strip() == "":
            raise ValueError("This field cannot be empty.")
        if value not in valid_cc2_ans:
            raise ValueError ("Answer must be in one of the choices.")
        return value
    
    @field_validator("cc3")
    @classmethod
    def validate_cc3(cls, value):
        valid_cc3_ans = [
            "Helped very much", 
            "Somewhat helped",
            "Did not help",
            "N/A"
            ]
        if value.strip() == "":
            raise ValueError("This field cannot be empty.")
        if value not in valid_cc3_ans:
            raise ValueError ("Answer must be in one of the choices.")
        return value   

CSV_HEADERS = [
    "service_id",
    "service_availed",
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

@router.post("/Submit_survey_response", response_model=SuccessResponse)
def post_response(response: SurveyResponse):
    try:

        with DATA_FILE.open("a", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=CSV_HEADERS)

            writer.writerow({
                "service_id": response.service_id,
                "service_availed": response.service_availed,
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

        return { "Message": "Survey submitted successfully."}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Could not save survey response: {exc}")