from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

email = "test4@example.com"
password = "test65432"

res = supabase.auth.sign_in_with_password({
    "email": email,
    "password": password
})

print("\nACCESS TOKEN:\n")
print(res.session.access_token)
