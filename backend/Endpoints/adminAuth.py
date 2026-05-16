from pathlib import Path
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import csv
import hashlib

router = APIRouter()

# --- PATH SETUP ---
DATA_DIR = Path(__file__).resolve().parents[2] / "data" 
ADMINS_FILE = DATA_DIR / "Admins.csv"
SERVICES_FILE = DATA_DIR / "Services.csv"

# Optional: Print paths on startup for debugging
print("--- DATABASE PATHS ---")
print(f"Admins File:   {ADMINS_FILE}")
print(f"Services File: {SERVICES_FILE}")
print("----------------------")

# --- PYDANTIC MODEL ---
class UserCredentials(BaseModel):
    username: str
    password: str
    service_id: str 

def _hash_password(password: str, salt: bytes) -> bytes:
    """Hashes the password using PBKDF2 with SHA-256."""
    return hashlib.pbkdf2_hmac(
        'sha256', 
        password.encode('utf-8'), 
        salt, 
        100000
    )

# =====================================================================
# VALIDATION LOGIC (Reads directly from CSVs)
# =====================================================================

def verify_admin_access(user: UserCredentials):
    """
    Handles all validation logic by reading the CSV files live.
    If it fails, it throws an HTTP error. If it succeeds, it passes the data forward.
    """
    # Failsafe: Ensure files actually exist before attempting to read them
    if not ADMINS_FILE.exists() or not SERVICES_FILE.exists():
        raise HTTPException(
            status_code=500, 
            detail="Database Error: CSV files are missing."
        )

    # 1. Check if the requested service exists in Services.csv
    service_exists = False
    attempted_service_name = ""
    
    with SERVICES_FILE.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row.get("service_id", "").strip() == user.service_id:
                service_exists = True
                attempted_service_name = row.get("service_name", "").strip()
                break

    if not service_exists:
        raise HTTPException(
            status_code=404, 
            detail=f"Service not found: ID '{user.service_id}' does not exist in the system."
        )

    # 2. Check Admin Credentials & Authorization in Admins.csv
    is_authenticated = False
    is_authorized = False

    with ADMINS_FILE.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Look for the specific user row
            if row.get("username", "").strip() == user.username:
                salt_hex = row.get("salt", "").strip()
                hash_hex = row.get("pwd_hash", "").strip()
                authorized_service_id = row.get("service_id", "").strip()
                
                # Check Password (Authentication)
                if salt_hex and hash_hex:
                    try:
                        stored_salt = bytes.fromhex(salt_hex)
                        stored_hash = bytes.fromhex(hash_hex)
                        login_hash = _hash_password(user.password, stored_salt)
                        
                        if stored_hash == login_hash:
                            is_authenticated = True
                    except ValueError:
                        pass # Ignore corrupted hex strings
                
                # Check Service Ownership (Authorization)
                if authorized_service_id == user.service_id:
                    is_authorized = True
                    
                break # We found the user, no need to keep reading the rest of the CSV

    # 3. Unified Rejection (Anti-enumeration)
    if not (is_authenticated and is_authorized):
        raise HTTPException(
            status_code=401, 
            detail="Invalid username or password."
        )

    # 4. Return the validated payload
    return {
        "username": user.username,
        "service_id": user.service_id,
        "service_name": attempted_service_name
    }

# =====================================================================
# ENDPOINTS
# =====================================================================

@router.post("/login")
def login_admin(verified_user: dict = Depends(verify_admin_access)):
    """Authenticates an admin by verifying against the live CSV data."""
    return {
        "message": "Login successful.", 
        **verified_user  
    }


@router.get("/services")
def get_services():
    """Reads Services.csv on the fly and returns the available services."""
    if not SERVICES_FILE.exists():
        raise HTTPException(status_code=500, detail="Database error: Services.csv file not found.")
        
    services = []
    with SERVICES_FILE.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            s_id = row.get("service_id", "").strip()
            s_name = row.get("service_name", "").strip()
            if s_id and s_name:
                services.append({"service_id": s_id, "service_name": s_name})
                
    return {"services": services}