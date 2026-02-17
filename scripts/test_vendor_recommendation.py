import os
from dotenv import load_dotenv
from supabase import create_client
from services.vendor_recommendation import recommend_vendors

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY"),
)


def main() -> None:
    vendors = recommend_vendors(
        supabase=supabase,
        category="photographers",
        city="lahore",            
        max_budget=3000,
        style_tags=None,
        limit=5,
    )

    print(f"Found {len(vendors)} vendors:\n")

    for v in vendors:
        print(
            f"- {v['name']} | {v['city']} | "
            f"{v['recommended_price']} | {v['style_tags']}"
        )


if __name__ == "__main__":
    main()
