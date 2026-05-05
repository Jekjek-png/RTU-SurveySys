import os
from supabase import Client, create_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SERVICEROLE_KEY = os.getenv("SERVICEROLE_KEY")

supabase = Client(SUPABASE_URL, SUPABASE_KEY)

def get_all_cars():
    try:
        response = supabase.table("Admin_Account_table").select("*").execute()
        return response.data
    except Exception as e:
        print("Error:", e)
        return None

cars = get_all_cars()
print(cars)