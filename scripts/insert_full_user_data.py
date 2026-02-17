from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY")
)

users_data = [
    {
        "id": "8336e7a6-48ae-439a-9299-795e4067aab8",
        "wedding_date": "2026-03-15",
        "budget": 30000,
        "style": "traditional",
        "guest_count": 250,
        "venue": "Pearl Continental Lahore",
        "celebrant": "Ahmed Qadri"
    },
    {
        "id": "b1d8ee8f-495a-41c4-8ce8-469c1e8b1330",
        "wedding_date": "2026-04-10",
        "budget": 45000,
        "style": "modern",
        "guest_count": 180,
        "venue": "Marriott Karachi",
        "celebrant": "Fatima Noor"
    },
    {
        "id": "32fb9c16-5c1f-4e84-80c2-a73587386084",
        "wedding_date": "2026-05-22",
        "budget": 80000,
        "style": "luxury",
        "guest_count": 400,
        "venue": "Serena Islamabad",
        "celebrant": "Mufti Salman"
    },
    {
        "id": "aae7cbaa-ee98-48ff-ab74-8b2e66354ab6",
        "wedding_date": "2026-06-05",
        "budget": 20000,
        "style": "simple",
        "guest_count": 120,
        "venue": "Community Hall Rawalpindi",
        "celebrant": "Hafiz Bilal"
    },
    {
        "id": "36696b79-cffd-4d71-84c6-a0f98f941567",
        "wedding_date": "2026-07-18",
        "budget": 38000,
        "style": "traditional",
        "guest_count": 220,
        "venue": "Grand Marquee Faisalabad",
        "celebrant": "Qari Imran"
    },
    {
        "id": "3b00af72-da3a-459e-8960-c665026d8cca",
        "wedding_date": "2026-08-02",
        "budget": 52000,
        "style": "modern",
        "guest_count": 300,
        "venue": "Multan Marquee",
        "celebrant": "Ayesha Siddiqua"
    },
    {
        "id": "6af10c07-152c-472d-b5d9-86cfac516ab3",
        "wedding_date": "2026-09-12",
        "budget": 60000,
        "style": "classic",
        "guest_count": 350,
        "venue": "Royal Palace Peshawar",
        "celebrant": "Mufti Hamid"
    },
    {
        "id": "5fcd27e6-1ae2-44ce-a6e9-f714d359e287",
        "wedding_date": "2026-10-25",
        "budget": 35000,
        "style": "boho",
        "guest_count": 200,
        "venue": "Quetta Serena Lawn",
        "celebrant": "Sana Rehman"
    },
    {
        "id": "aada85cf-426a-4645-82b1-adfdc8a07b4e",
        "wedding_date": "2026-11-08",
        "budget": 75000,
        "style": "luxury",
        "guest_count": 450,
        "venue": "Sialkot Golf Club",
        "celebrant": "Dr. Khalid"
    },
    {
        "id": "1a6eda87-2fb0-4dfe-b011-b21c3f74308a",
        "wedding_date": "2026-12-20",
        "budget": 48000,
        "style": "modern",
        "guest_count": 280,
        "venue": "Hyderabad Banquet",
        "celebrant": "Rabia Anjum"
    }
]

for user in users_data:
    supabase.table("users").update({
        "wedding_date": user["wedding_date"],
        "budget": user["budget"],
        "style": user["style"],
        "guest_count": user["guest_count"],
        "venue": user["venue"],
        "celebrant": user["celebrant"]
    }).eq("id", user["id"]).execute()

    print(f"Wedding data inserted for USER_ID: {user['id']}")
