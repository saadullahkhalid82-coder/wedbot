from app.db import supabase


def update_user_detail(user_id: str, field: str, value):
    supabase.table("users").update({
        field: value
    }).eq("id", user_id).execute()


def get_user_detail(user_id: str, field: str):
    response = (
        supabase
        .table("users")
        .select(field)
        .eq("id", user_id)
        .single()
        .execute()
    )
    return response.data.get(field)

def get_all_user_details(user_id: str) -> dict:
    response = (
        supabase
        .table("users")
        .select(
            "style, budget, guest_count, venue, wedding_date, celebrant"
        )
        .eq("id", user_id)
        .single()
        .execute()
    )
    return response.data

