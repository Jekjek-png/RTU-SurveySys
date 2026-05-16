from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, Query
import csv
from datetime import datetime
from collections import Counter, defaultdict
from .admin_auth import verify_admin_access

router = APIRouter()

DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "Survey_response.csv"

@router.post("/service_summary")
def get_service_summary(
    verified_user: dict = Depends(verify_admin_access),
    start_date: str = Query(None, description="Start date in MM-DD-YYYY"),
    end_date: str = Query(None, description="End date in MM-DD-YYYY")
):
   
  #  Summarizes survey responses exclusively for the service assigned to the logged-in admin.
    if not DATA_FILE.exists():
        raise HTTPException(status_code=500, detail="Survey response data file not found.")

    service_id = verified_user.get("service_id")
    service_name = verified_user.get("service_name")
    
    # Pre-parse dates.
    sd_obj = None
    ed_obj = None
    try:
        if start_date: sd_obj = datetime.strptime(start_date.strip(), "%m-%d-%Y")
        if end_date: ed_obj = datetime.strptime(end_date.strip(), "%m-%d-%Y")
    except ValueError:
        raise HTTPException(
            status_code=400, 
            detail="Invalid date format. Please use MM-DD-YYYY with dashes (e.g., 05-15-2026)."
        )

    rating_fields = {
        "service_satisfaction": "service_satisfaction(1-5)",
        "service_time": "service_time(1-5)",
        "service_requirements": "service_requirements(1-5)",
        "service_steps": "service_steps(1-5)",
        "service_transaction": "service_transaction(1-5)",
        "service_fee": "service_fee(1-5 or n/a)",
        "service_fair": "service_fair(1-5)",
        "service_courtesy": "service_courtesy(1-5)",
        "service_request": "service_request(1-5)"
    }
    
    # Data structures optimized for fast counting
    total_responses = 0
    rating_sums = defaultdict(float)
    rating_counts = Counter()
    
    demographics = {
        "gender": Counter(),
        "age_bracket": Counter(),
        "category_of_respondent": Counter()
    }
    
    cc_counts = {"cc1": Counter(), "cc2": Counter(), "cc3": Counter()}
    
    comments_general = []
    comments_employee = []
    
    with DATA_FILE.open(mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        
        # Clean headers once. This allows us to handle any extra spaces or case issues in the CSV headers without doing it repeatedly inside the loop.
        if reader.fieldnames:
            reader.fieldnames = [str(fn).strip().lower() for fn in reader.fieldnames]

        for row in reader:
            # Exit on service mismatch. This ensures we only process relevant rows and skip the rest immediately.
            if row.get("service_id", "").strip() != service_id:
                continue
                
            # Date filtering
            if sd_obj or ed_obj:
                try:
                    row_date = datetime.strptime(row.get("date_of_visit", "").strip(), "%d/%m/%Y")
                    if sd_obj and row_date < sd_obj: continue
                    if ed_obj and row_date > ed_obj: continue
                except ValueError:
                    continue 
                    
            total_responses += 1
            
            # Process ratings. 
            for metric, csv_key in rating_fields.items():
                val = row.get(csv_key, "").strip()
                if val and val.lower() != "n/a":
                    try:
                        rating_sums[metric] += float(val)
                        rating_counts[metric] += 1
                    except ValueError:
                        pass
            
            # Process demographics automatically with Counter.
            demographics["gender"][row.get("gender", "Unknown").strip() or "Unknown"] += 1
            demographics["age_bracket"][row.get("age_bracket", "Unknown").strip() or "Unknown"] += 1
            demographics["category_of_respondent"][row.get("category_of_respondent", "Unknown").strip() or "Unknown"] += 1
            
            # Process Citizen Charter.
            for cc in cc_counts.keys():
                cc_val = row.get(cc, "").strip().lower()
                if cc_val in ["yes", "no"]:
                    cc_counts[cc][cc_val] += 1
            
            # Process Comments.
            gen_comment = row.get("comments_suggestions", "").strip()
            emp_comment = row.get("comments_suggestions_for_employee", "").strip()
            
            if gen_comment and gen_comment.lower() != "n/a":
                comments_general.append(gen_comment)
            if emp_comment and emp_comment.lower() != "n/a":
                comments_employee.append(emp_comment)
                    
    # Compute final averages natively.
    averages = {}
    for metric in rating_fields:
        if rating_counts[metric] > 0:
            averages[metric] = round(rating_sums[metric] / rating_counts[metric], 2)
        else:
            averages[metric] = "N/A"
            
    return {
        "status": "success",
        "service_id": service_id,
        "service_name": service_name,
        "total_responses": total_responses,
        "averages": averages,
        "demographics": demographics,
        "citizen_charter": cc_counts,
        "feedback": {
            "general_comments": comments_general,
            "employee_comments": comments_employee
        }
    }