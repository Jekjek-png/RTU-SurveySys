import os
import hashlib
import csv
from pathlib import Path

# Dynamically finds the Data folder.
DATA_DIR = Path(__file__).resolve().parents[2] / "data" 
ADMINS_FILE = DATA_DIR / "Admins.csv"

# Premade Accounts
accounts_to_create = [
    {"username": "accAdmin", "password": "accAdmin123!", "service_id": "SV001"},
    {"username": "clinicAdmin", "password": "clinicAdmin456!", "service_id": "SV002"},
    {"username": "registrarAdmin", "password": "registrarAdmin789!", "service_id": "SV003"}
]

def _hash_password(password: str, salt: bytes) -> bytes:
    """The exact same hashing engine used in your main app."""
    return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

def generate_real_csv():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    print(f"Generating mathematically correct hashes in {ADMINS_FILE}...")
    
    with ADMINS_FILE.open(mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        writer.writerow(["username", "salt", "pwd_hash", "service_id"])
        
        for account in accounts_to_create:
            real_salt = os.urandom(16)
            real_hash = _hash_password(account["password"], real_salt)
            writer.writerow([
                account["username"], 
                real_salt.hex(), 
                real_hash.hex(), 
                account["service_id"]
            ])
            print(f" -> Success: Account '{account['username']}' generated.")
            
    print("Done! You can now start your server and log in.")

if __name__ == "__main__":
    generate_real_csv()