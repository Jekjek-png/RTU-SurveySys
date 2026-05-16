from pathlib import Path
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import csv
import hashlib

router = APIRouter()

# PATH SETUP 
DATA_DIR = Path(__file__).resolve().parents[2] / "data" 
ADMINS_FILE = DATA_DIR / "Admins.csv"
SERVICES_FILE = DATA_DIR / "Services.csv"

# PYDANTIC MODELS
class LoginCredentials(BaseModel):
    username: str
    password: str

# PASSWORD HASHING LOGIC
def _hash_password(password: str, salt: bytes) -> bytes:
    """Hashes the password using PBKDF2 with SHA-256."""
    return hashlib.pbkdf2_hmac(
        'sha256', 
        password.encode('utf-8'), 
        salt, 
        100000
    )

# VALIDATION LOGIC 

def verify_admin_access(credentials: LoginCredentials):
  
    # Authenticates the ADMIN securely via request body and retrieves their assigned Service_ID.
    if not ADMINS_FILE.exists() or not SERVICES_FILE.exists():
        raise HTTPException(
            status_code=500, 
            detail="Database Error: CSV files are missing."
        )

    is_authenticated = False
    authorized_service_id = ""

    # 1. Authenticate ADMIN and get their assigned Service_ID
    with ADMINS_FILE.open(mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row.get("username", "").strip() == credentials.username:
                salt_hex = row.get("salt", "").strip()
                hash_hex = row.get("pwd_hash", "").strip()
                
                if salt_hex and hash_hex:
                    try:
                        stored_salt = bytes.fromhex(salt_hex)
                        stored_hash = bytes.fromhex(hash_hex)
                        login_hash = _hash_password(credentials.password, stored_salt)
                        
                        # Use standard equality check
                        if stored_hash == login_hash:
                            is_authenticated = True
                            authorized_service_id = row.get("service_id", "").strip()
                    except ValueError:
                        pass 
                
                break 

    if not is_authenticated:
        raise HTTPException(
            status_code=401, 
            detail="Invalid username or password."
        )

    # 2. Look up the human-readable service name
    assigned_service_name = "Unknown Service"
    with SERVICES_FILE.open(mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row.get("service_id", "").strip() == authorized_service_id:
                assigned_service_name = row.get("service_name", "").strip()
                break

    return {
        "username": credentials.username,
        "service_id": authorized_service_id,
        "service_name": assigned_service_name
    }

# ENDPOINTS


@router.post("/login")
def login_admin(verified_user: dict = Depends(verify_admin_access)):
    # Authenticates an ADMIN and returns their assigned service details.
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
    with SERVICES_FILE.open(mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            s_id = row.get("service_id", "").strip()
            s_name = row.get("service_name", "").strip()
            if s_id and s_name:
                services.append({"service_id": s_id, "service_name": s_name})
                
    return {"services": services}