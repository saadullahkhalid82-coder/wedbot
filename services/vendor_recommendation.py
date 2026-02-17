from __future__ import annotations
from typing import List, Optional, Dict, Any
from supabase import Client


def recommend_vendors(
    supabase: Client,
    *,
    category: str,
    city: str,
    max_budget: int,
    style_tags: Optional[List[str]] = None,
    limit: int = 10,
) -> List[Dict[str, Any]]:
    """
    Recommend vendors based on category, city, budget, and optional style tags.
    """

    query = (
        supabase
        .table("vendors")
        .select("*")
        .eq("category", category.lower())
        .eq("city", city.lower())
        .lte("recommended_price", max_budget)
        .limit(limit)
    )

    if style_tags:
        # overlap operator for Postgres array
        query = query.contains("style_tags", style_tags)

    response = query.execute()

    if not response.data:
        return []

    return response.data
