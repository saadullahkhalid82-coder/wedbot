import os
from dotenv import load_dotenv
from supabase import create_client
from services.vendor_recommendation import recommend_vendors
from services.vendor_comparison_ai import generate_vendor_comparison

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
        limit=5,
    )

    print(f"[INFO] {len(vendors)} vendors selected for comparison\n")

    summary = generate_vendor_comparison(
        vendors,
        budget=3000,
        category="photographers",
    )

    print("=== AI COMPARISON OUTPUT ===\n")
    print(summary)


if __name__ == "__main__":
    main()
