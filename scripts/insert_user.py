from supabase import create_client
from dotenv import load_dotenv
import os
import uuid

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY")
)

users = [
    "ali.hassan@wedlii.com",
    "sara.ahmed@wedlii.com",
    "usman.raza@wedlii.com",
    "ayesha.noor@wedlii.com",
    "hamza.sheikh@wedlii.com",
    "nida.malik@wedlii.com",
    "bilal.hussain@wedlii.com",
    "zainab.tariq@wedlii.com",
    "farhan.ali@wedlii.com",
    "hira.iqbal@wedlii.com"
]

created_users = []

for email in users:
    user_id = str(uuid.uuid4())

    supabase.table("users").insert({
        "id": user_id,
        "email": email,
        "password": "demo123"
    }).execute()

    created_users.append(user_id)

    print(f"Created user: {email}")
    print(f"USER_ID: {user_id}")

print("\nSAVE THESE USER_IDS — REQUIRED FOR NEXT FILE")
print(created_users)
