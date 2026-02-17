import os
from dotenv import load_dotenv
from supabase import create_client

from services.vendor_shortlist import (
    add_to_shortlist,
    get_shortlist,
    remove_from_shortlist,
)

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY"),
)

USER_ID = "00000001-0000-0000-0000-000000000001"


def main() -> None:
    vendor = (
        supabase
        .table("vendors")
        .select("id, name")
        .limit(1)
        .execute()
        .data[0]
    )

    print(f"[TEST] Using vendor: {vendor['name']}")

    # ADD
    add_to_shortlist(
        supabase=supabase,
        user_id=USER_ID,
        vendor_id=vendor["id"],
    )
    print("[OK] Vendor added to shortlist")

    # LIST
    shortlist = get_shortlist(
        supabase=supabase,
        user_id=USER_ID,
    )
    print(f"[OK] Shortlist contains {len(shortlist)} vendors")

    # REMOVE
    remove_from_shortlist(
        supabase=supabase,
        user_id=USER_ID,
        vendor_id=vendor["id"],
    )
    print("[OK] Vendor removed from shortlist")


if __name__ == "__main__":
    main()
