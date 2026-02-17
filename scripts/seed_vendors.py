from __future__ import annotations
import os
import uuid
from typing import List, Dict
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Missing Supabase credentials")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)



VENDORS: List[Dict] = [
    
    {
        "name": "Golden Frame Studios",
        "category": "photographers",
        "style_tags": ["romantic", "classic"],
        "city": "lahore",
        "recommended_price": 2500,
    },
    {
        "name": "Rustic Lens Co.",
        "category": "photographers",
        "style_tags": ["rustic", "outdoor"],
        "city": "lahore",
        "recommended_price": 3000,
    },
    {
        "name": "Modern Moments",
        "category": "photographers",
        "style_tags": ["modern", "minimal"],
        "city": "karachi",
        "recommended_price": 4000,
    },

    
    {
        "name": "Rosewood Garden Venue",
        "category": "venues",
        "style_tags": ["outdoor", "garden"],
        "city": "lahore",
        "recommended_price": 8000,
    },
    {
        "name": "Royal Banquet Hall",
        "category": "venues",
        "style_tags": ["luxury", "classic"],
        "city": "karachi",
        "recommended_price": 12000,
    },

    
    {
        "name": "Bloom & Petal",
        "category": "florists",
        "style_tags": ["romantic", "pastel"],
        "city": "lahore",
        "recommended_price": 1500,
    },
    {
        "name": "Urban Floral Studio",
        "category": "florists",
        "style_tags": ["modern", "minimal"],
        "city": "karachi",
        "recommended_price": 2000,
    },
]


def main() -> None:
    payload = []

    for v in VENDORS:
        payload.append({
            "id": str(uuid.uuid4()),
            "name": v["name"],
            "category": v["category"],
            "style_tags": v["style_tags"],
            "city": v["city"],
            "recommended_price": v["recommended_price"],
            "availability": None,
            "source_url": f"seed://{v['name'].lower().replace(' ', '-')}",
        })

    supabase.table("vendors").upsert(
        payload,
        on_conflict="source_url"
    ).execute()

    print(f"[DONE] Seeded {len(payload)} vendors")


if __name__ == "__main__":
    main()
