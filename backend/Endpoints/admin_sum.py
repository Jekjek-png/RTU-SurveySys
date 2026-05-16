from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from .admin_auth import verify_admin_access

router = APIRouter()

DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "Survey_response.csv"

@router.post("/service_summary")
def get_service_summary(
    verified_user: dict = Depends(verify_admin_access),
    preset_range: str = Query(None, description="Preset date range. Options: 'today', 'last_week', 'last_month', 'current_year', 'last_year'")
):
 
  #  Summarizes survey responses exclusively for the service assigned to the logged-in admin.

    if not DATA_FILE.exists():
        raise HTTPException(status_code=500, detail="Survey response data file not found.")

    service_id = verified_user.get("service_id")
    service_name = verified_user.get("service_name")
    
    # DATE PRESET LOGIC

    sd_obj = None
    ed_obj = None
    
    current_date = datetime.now()
    
    if preset_range:
        preset_range = preset_range.lower().strip()
        
        # Dictionary mapping.
        preset_map = {
            "today": (current_date - timedelta(days=1), current_date),
            "last_week": (current_date - timedelta(days=7), current_date),
            "last_month": (current_date - timedelta(days=30), current_date),
            "current_year": (datetime(current_date.year, 1, 1), current_date),
            "last_year": (datetime(current_date.year - 1, 1, 1), datetime(current_date.year - 1, 12, 31))
        }
        
        # Instantly fetch the tuple and unpack it into our start and end date variables.
        if preset_range in preset_map:
            sd_obj, ed_obj = preset_map[preset_range]
        else:
            raise HTTPException(status_code=400, detail=f"Invalid preset_range option: '{preset_range}'")

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
    
    # Load data using Pandas
    try:
        df = pd.read_csv(DATA_FILE, dtype=str)
    except Exception:
        raise HTTPException(status_code=500, detail="Error reading the survey response data file.")
        
    # Clean headers: lowercase and strip whitespace
    df.columns = df.columns.str.strip().str.lower()
    
    # Security & Performance: Filter strictly by the admin's assigned Service_ID
    if 'service_id' in df.columns:
        df['service_id'] = df['service_id'].str.strip()
        df = df[df['service_id'] == service_id]
    else:
        df = pd.DataFrame() 

    # Date filtering via vectorized boolean masking
    if not df.empty and (sd_obj or ed_obj):
        if 'date_of_visit' in df.columns:
            dates = pd.to_datetime(df['date_of_visit'].str.strip(), format="%d/%m/%Y", errors='coerce')
            
            mask = pd.Series(True, index=df.index)
            if sd_obj:
                mask &= (dates >= sd_obj)
            if ed_obj:
                mask &= (dates <= ed_obj)
                
            df = df[mask]
            
    total_responses = len(df)
    
    # Initialize response structures
    averages = {}
    demographics = {"gender": {}, "age_bracket": {}, "category_of_respondent": {}}
    
    cc_counts = {
        "cc1": {"Option A": 0, "Option B": 0, "Option C": 0, "Option D": 0}, 
        "cc2": {"Option A": 0, "Option B": 0, "Option C": 0, "Option D": 0}, 
        "cc3": {"Option A": 0, "Option B": 0, "Option C": 0, "Option D": 0}
    }
    
    comments_general = []
    comments_employee = []
    
    if total_responses > 0:
        # Process Ratings
        for metric, csv_key in rating_fields.items():
            if csv_key in df.columns:
                s = df[csv_key].str.strip()
                s = s.replace(r'(?i)^n/a$', np.nan, regex=True).replace('', np.nan)
                s = pd.to_numeric(s, errors='coerce')
                
                if s.notna().sum() > 0:
                    averages[metric] = round(s.mean(), 2)
                else:
                    averages[metric] = "N/A"
            else:
                averages[metric] = "N/A"
                
        # Process Demographics.
        for demo_key in demographics.keys():
            if demo_key in df.columns:
                s = df[demo_key].str.strip().replace('', 'Unknown').fillna('Unknown')
                demographics[demo_key] = s.value_counts().to_dict()
                
        # Process Citizen Charter.
        for cc in cc_counts.keys():
            if cc in df.columns:
                s = df[cc].str.strip().str.title()
                counts = s.value_counts().to_dict()
                
                cc_counts[cc]["Option A"] = counts.get("Option A", 0)
                cc_counts[cc]["Option B"] = counts.get("Option B", 0)
                cc_counts[cc]["Option C"] = counts.get("Option C", 0)
                cc_counts[cc]["Option D"] = counts.get("Option D", 0)
                
        # Process Feedback
        if "comments_suggestions" in df.columns:
            s = df["comments_suggestions"].str.strip()
            mask = (s != "") & (s.str.lower() != "n/a") & s.notna()
            comments_general = s[mask].tolist()
            
        if "comments_suggestions_for_employee" in df.columns:
            s = df["comments_suggestions_for_employee"].str.strip()
            mask = (s != "") & (s.str.lower() != "n/a") & s.notna()
            comments_employee = s[mask].tolist()
            
    else:
        for metric in rating_fields:
            averages[metric] = "N/A"

    return {
        "status": "success",
        "service_id": service_id,
        "service_name": service_name,
        "total_responses": int(total_responses),
        "active_filter": preset_range if preset_range else "all",
        "averages": averages,
        "demographics": demographics,
        "citizen_charter": cc_counts,
        "feedback": {
            "general_comments": comments_general,
            "employee_comments": comments_employee
        }
    }