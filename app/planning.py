from typing import List, Dict
import json
import openai

from app.db import supabase
from app.config import OPENAI_API_KEY
from app.prompts import CHECKLIST_PROMPT

openai.api_key = OPENAI_API_KEY

def create_checklist(user_id: str, title: str, tasks: List[str]) -> str:
    checklist = supabase.table("checklists").insert({
        "user_id": user_id,
        "title": title
    }).execute()

    checklist_id = checklist.data[0]["id"]

    rows = [
        {
            "checklist_id": checklist_id,
            "user_id": user_id,
            "title": task,
            "status": "pending"
        }
        for task in tasks
    ]

    supabase.table("tasks").insert(rows).execute()
    return checklist_id


def add_task(user_id: str, title: str) -> None:
    supabase.table("tasks").insert({
        "user_id": user_id,
        "title": title,
        "status": "pending"
    }).execute()


def complete_task(user_id: str, title: str) -> None:
    supabase.table("tasks") \
        .update({"status": "completed"}) \
        .eq("user_id", user_id) \
        .ilike("title", f"%{title}%") \
        .execute()


def get_tasks(user_id: str, status: str = "pending"):
    return supabase.table("tasks") \
        .select("title,status") \
        .eq("user_id", user_id) \
        .eq("status", status) \
        .execute().data


def create_ai_checklist(user_id: str, user_context: dict) -> int:
    from app.prompts import CHECKLIST_PROMPT

    prompt = CHECKLIST_PROMPT.format(
        style=user_context.get("style"),
        budget=user_context.get("budget"),
        guest_count=user_context.get("guest_count"),
        wedding_date=user_context.get("wedding_date"),
    )

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.choices[0].message["content"].strip()

    if raw.startswith("```"):
        raw = raw.replace("```json", "").replace("```", "").strip()

    try:
        tasks = json.loads(raw)
    except Exception as e:
        raise ValueError(f"Checklist AI returned invalid JSON: {raw}") from e

    checklist = supabase.table("checklists").insert({
        "user_id": user_id,
        "title": "Wedding Checklist"
    }).execute()

    checklist_id = checklist.data[0]["id"]

    rows = [
        {
            "user_id": user_id,
            "checklist_id": checklist_id,
            "title": task,
            "status": "pending"
        }
        for task in tasks
    ]

    supabase.table("tasks").insert(rows).execute()
    return len(rows)


def create_timeline(user_id: str, blocks: List[Dict[str, str]]) -> None:
    """
    blocks example:
    [
      {"label": "Ceremony", "start": "16:00", "end": "16:30"},
      {"label": "Reception", "start": "18:00", "end": "22:00"}
    ]
    """
    supabase.table("timelines").delete().eq("user_id", user_id).execute()

    supabase.table("timelines").insert([
        {
            "user_id": user_id,
            "label": block["label"],
            "start_time": block["start"],
            "end_time": block["end"]
        }
        for block in blocks
    ]).execute()
    
def create_default_timeline(user_id: str, style: str | None) -> int:
    """
    Creates a default wedding-day timeline based on style
    """

    # clear existing timeline
    supabase.table("timelines").delete().eq("user_id", user_id).execute()

    # base timeline
    blocks = [
        {"label": "Guest arrival", "start": "15:30", "end": "16:00"},
        {"label": "Ceremony", "start": "16:00", "end": "16:30"},
        {"label": "Cocktail hour", "start": "16:30", "end": "17:30"},
        {"label": "Reception entry", "start": "17:30", "end": "18:00"},
        {"label": "Dinner", "start": "18:00", "end": "19:30"},
        {"label": "First dance", "start": "19:30", "end": "19:45"},
        {"label": "Open dancing", "start": "19:45", "end": "22:00"},
        {"label": "Send-off", "start": "22:00", "end": "22:15"}
    ]

    
    if style == "casual":
        blocks = blocks[:-1]  
    elif style == "formal":
        blocks.append({"label": "Late night snacks", "start": "22:15", "end": "22:45"})

    supabase.table("timelines").insert([
        {
            "user_id": user_id,
            "label": b["label"],
            "start_time": b["start"],
            "end_time": b["end"]
        }
        for b in blocks
    ]).execute()

    return len(blocks)


def create_budget_breakdown(user_id: str, total_budget: float) -> None:
    breakdown = {
        "Venue": 0.4,
        "Catering": 0.3,
        "Photography": 0.1,
        "Decor": 0.1,
        "Misc": 0.1
    }

    supabase.table("budget_categories").delete().eq("user_id", user_id).execute()

    rows = [
        {
            "user_id": user_id,
            "category": category,
            "allocated": total_budget * ratio,
            "spent": 0
        }
        for category, ratio in breakdown.items()
    ]

    supabase.table("budget_categories").insert(rows).execute()


def update_category_budget(user_id: str, category: str, amount: float) -> None:
    supabase.table("budget_categories") \
        .update({"allocated": amount}) \
        .eq("user_id", user_id) \
        .eq("category", category) \
        .execute()
