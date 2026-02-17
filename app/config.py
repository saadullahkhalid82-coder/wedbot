from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
SUPABASE_URL: str = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY: str = os.getenv("SUPABASE_SERVICE_KEY")
SUPABASE_JWT_SECRET: str = os.getenv("SUPABASE_JWT_SECRET")

if not SUPABASE_JWT_SECRET:
    raise RuntimeError("SUPABASE_JWT_SECRET missing from environment")

