from __future__ import annotations
from typing import List, Dict, Any
from supabase import Client


def add_to_shortlist(
    supabase: Client,
    *,
    user_id: str,
    vendor_id: str,
) -> None:
    supabase.table("vendor_shortlist").insert({
        "user_id": user_id,
        "vendor_id": vendor_id,
    }).execute()


def get_shortlist(
    supabase: Client,
    *,
    user_id: str,
) -> List[Dict[str, Any]]:
    response = (
        supabase
        .table("vendor_shortlist")
        .select("vendors(*)")
        .eq("user_id", user_id)
        .execute()
    )

    return [row["vendors"] for row in response.data] if response.data else []


def remove_from_shortlist(
    supabase: Client,
    *,
    user_id: str,
    vendor_id: str,
) -> None:
    supabase.table("vendor_shortlist") \
        .delete() \
        .eq("user_id", user_id) \
        .eq("vendor_id", vendor_id) \
        .execute()
