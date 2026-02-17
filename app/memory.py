from app.db import supabase

MAX_TURNS = 10


def get_conversation(user_id: str) -> list[dict]:
    response = (
        supabase
        .table("conversation_buffer")
        .select("role,message")
        .eq("user_id", user_id)
        .order("created_at")
        .limit(MAX_TURNS)
        .execute()
    )

    history = []

    for row in response.data or []:
        history.append({
            "role": row["role"],
            "content": row["message"] 
        })

    return history


def save_message(user_id: str, role: str, message: str):

    message = message or ""

    supabase.table("conversation_buffer").insert({
        "user_id": user_id,
        "role": role,
        "message": message 
    }).execute()

    rows = (
        supabase
        .table("conversation_buffer")
        .select("id")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .execute()
        .data
    )

    if len(rows) > MAX_TURNS:
        ids_to_delete = [r["id"] for r in rows[MAX_TURNS:]]
        supabase.table("conversation_buffer") \
            .delete() \
            .in_("id", ids_to_delete) \
            .execute()
