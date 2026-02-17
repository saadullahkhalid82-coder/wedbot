from supabase import create_client
from dotenv import load_dotenv
import os
import uuid


load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")


if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
 raise ValueError("Supabase credentials not found in .env")


supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)


user_id = str(uuid.uuid4())

insert_response = supabase.table("users").insert({
    "id": user_id,
    "email": "test@wedlii.com",
    "password": "test123",
    "guest_count": 100
}).execute()


fetch_response = (
    supabase
    .table("users")
    .select("*")
    .eq("id", user_id)
    .execute()
)

print("SUPABASE CONNECTION SUCCESSFUL")
print(fetch_response.data)
