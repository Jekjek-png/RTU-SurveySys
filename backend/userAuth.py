import os
from dotenv import load_dotenv
from supabase import create_client, Client
from passlib.context import CryptContext

# ✅ Load environment variables
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ✅ Password hashing context (Argon2 recommended)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def account_record(username: str, password: str, role: str):
    """Insert a new account row into Admin_Account_table with hashed password."""
    hashed_pw = pwd_context.hash(password)
    data = {
        "Username": username,
        "Password_hash": hashed_pw,   # column must be TEXT
        "Service_role": role
    }
    response = supabase.table("Admin_Account_table").insert(data).execute()
    return response

def account_create():
    """Prompt user for account details and insert into Supabase."""
    name = input("Enter username: ")
    password = input("Enter password: ")
    role = input("Enter role (admin/user): ")

    response = account_record(name, password, role)

    if response.data:
        print("Account created successfully!")
        print("Inserted row:", response.data)
    else:
        print("Failed to create account. Error:", response)

def account_login():
    """Prompt user for login and verify credentials."""
    name = input("Enter username: ")
    password = input("Enter password: ")
    role = input("Enter role (admin/user): ")

    response = supabase.table("Admin_Account_table").select("*").eq("Username", name).execute()

    if not response.data:
        print("Invalid username")
        return

    account = response.data[0]

    if not pwd_context.verify(password, account["Password_hash"]):
        print("Invalid password")
        return

    if account["Service_role"] != role:
        print("Invalid role")
        return

    print(f"Login successful! Welcome {account['Username']} ({account['Service_role']})")

if __name__ == "__main__":
    print("Choose an option:")
    print("1. Create account")
    print("2. Login")
    choice = input("Enter choice (1/2): ")

    if choice == "1":
        account_create()
    elif choice == "2":
        account_login()
    else:
        print("Invalid choice")
