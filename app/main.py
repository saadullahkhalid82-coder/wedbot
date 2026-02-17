from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import openai
import json
from datetime import datetime
import httpx

from app.config import OPENAI_API_KEY, SUPABASE_SERVICE_KEY, SUPABASE_URL
from app.db import supabase
from app.memory import get_conversation, save_message
from app.functions import update_user_detail, get_user_detail
from app.prompts import SYSTEM_PROMPT

from app.planning import (
    complete_task,
    get_tasks,
    create_ai_checklist,
    create_default_timeline,
    create_budget_breakdown
)

from app.exports import (
    export_tasks_csv,
    export_budget_pdf,
    export_checklist_pdf
)

openai.api_key = OPENAI_API_KEY
app = FastAPI(title="WedBot")

security = HTTPBearer()

def verify_token(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        response = httpx.get(
            f"{SUPABASE_URL}/auth/v1/user",
            headers={
                "Authorization": f"Bearer {token}",
                "apikey": SUPABASE_SERVICE_KEY,
            },
            timeout=5
        )

        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid token")

        user_data = response.json()
        user_id = user_data["id"]
        user_email = user_data.get("email")

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    db_user = (
        supabase
        .table("users")
        .select("role")
        .eq("id", user_id)
        .single()
        .execute()
        .data
    )

    if not db_user:
        raise HTTPException(status_code=403, detail="User not found")

    request.state.user = {
        "id": user_id,
        "email": user_email,
        "role": db_user.get("role", "bride")
    }


def require_roles(*allowed_roles):
    def checker(request: Request):
        user_role = request.state.user.get("role")

        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail=f"Role '{user_role}' not allowed for this action"
            )
    return checker

def generate_weekly_schedule(user_id: str):
    user = (
        supabase.table("users")
        .select("wedding_date")
        .eq("id", user_id)
        .single()
        .execute()
        .data
    )

    if not user or not user.get("wedding_date"):
        raise HTTPException(status_code=400, detail="Wedding date not set")

    wedding_date = datetime.fromisoformat(user["wedding_date"])
    today = datetime.utcnow()

    weeks_remaining = max(1, (wedding_date - today).days // 7)

    tasks = (
        supabase.table("tasks")
        .select("*")
        .eq("user_id", user_id)
        .eq("completed", False)
        .execute()
        .data
    )

    if not tasks:
        return 0

    total_tasks = len(tasks)
    tasks_per_week = max(1, total_tasks // weeks_remaining)

    week_counter = 1
    assigned = 0

    for task in tasks:
        supabase.table("tasks").update({
            "scheduled_week": week_counter,
            "updated_at": datetime.utcnow().isoformat()
        }).eq("id", task["id"]).execute()

        assigned += 1

        if assigned % tasks_per_week == 0 and week_counter < weeks_remaining:
            week_counter += 1

    return assigned


def log_audit_event(
    user_id: str,
    action_type: str,
    old_value,
    new_value,
    changed_by: str
):
    supabase.table("audit_logs").insert({
        "user_id": user_id,
        "action_type": action_type,
        "old_value": old_value,
        "new_value": new_value,
        "changed_by": changed_by,
        "created_at": datetime.utcnow().isoformat()
    }).execute()



class ChatRequest(BaseModel):
    message: str


class PortalMockUpdateRequest(BaseModel):
    field: str
    value: str


@app.get("/sync/changes")
def get_changes(
    since: str,
    request: Request,
    _: None = Depends(verify_token)
):
    user_id = request.state.user["id"]

    try:
        datetime.fromisoformat(since)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid timestamp format")

    user_changes = (
        supabase.table("users")
        .select("*")
        .eq("id", user_id)
        .gt("updated_at", since)
        .execute()
        .data
    )

    task_changes = (
        supabase.table("tasks")
        .select("*")
        .eq("user_id", user_id)
        .gt("updated_at", since)
        .execute()
        .data
    )

    budget_changes = (
        supabase.table("budget_categories")
        .select("*")
        .eq("user_id", user_id)
        .gt("updated_at", since)
        .execute()
        .data
    )

    return {
        "users": user_changes,
        "tasks": task_changes,
        "budget_categories": budget_changes
    }

@app.post("/portal/mock-update")
def portal_mock_update(
    req: PortalMockUpdateRequest,
    request: Request,
    _: None = Depends(verify_token)
):
    user_id = request.state.user["id"]

    allowed_fields = {
        "budget",
        "venue",
        "style",
        "wedding_date",
        "guest_count",
        "celebrant"
    }

    if req.field not in allowed_fields:
        raise HTTPException(status_code=400, detail="Invalid field")

    old_data = (
    supabase.table("users")
    .select(req.field)
    .eq("id", user_id)
    .single()
    .execute()
    .data
)

    supabase.table("users").update({
        req.field: req.value,
        "updated_at": datetime.utcnow().isoformat()
    }).eq("id", user_id).execute()

    log_audit_event(
        user_id=user_id,
        action_type=f"portal_update_{req.field}",
        old_value=old_data,
        new_value={req.field: req.value},
        changed_by="portal"
    )

@app.get("/tasks")
def fetch_tasks(
    request: Request,
    _: None = Depends(verify_token)
):
    return get_tasks(request.state.user["id"])

@app.post("/tasks/complete")
def mark_complete(
    title: str,
    request: Request,
    _: None = Depends(verify_token),
    __: None = Depends(require_roles("bride", "groom"))
):
    complete_task(request.state.user["id"], title)
    log_audit_event(
    user_id=request.state.user["id"],
    action_type="task_completed",
    old_value=None,
    new_value={"task": title},
    changed_by="chat"
)

    return {"status": "ok"}


@app.get("/export/tasks")
def export_tasks(
    request: Request,
    _: None = Depends(verify_token)
):
    return export_tasks_csv(request.state.user["id"])


@app.get("/export/budget")
def export_budget(
    request: Request,
    _: None = Depends(verify_token)
):
    return export_budget_pdf(request.state.user["id"])


@app.get("/export/checklist")
def export_checklist(
    request: Request,
    _: None = Depends(verify_token)
):
    return export_checklist_pdf(request.state.user["id"])

@app.post("/schedule/generate")
def schedule_generate(
    request: Request,
    _: None = Depends(verify_token),
    __: None = Depends(require_roles("bride", "groom"))
):
    user_id = request.state.user["id"]

    count = generate_weekly_schedule(user_id)
    log_audit_event(
    user_id=user_id,
    action_type="weekly_schedule_generated",
    old_value=None,
    new_value={"tasks_scheduled": count},
    changed_by="chat"
)


    return {
        "status": "weekly schedule generated",
        "tasks_scheduled": count
    }


STRESS_KEYWORDS = [
    "stressed", "overwhelmed", "anxious",
    "panic", "too much", "cant handle",
    "tired", "exhausted"
]


def get_random_wellness_content(content_type: str):
    result = (
        supabase
        .table("wellness_content")
        .select("title, content")
        .eq("type", content_type)
        .limit(1)
        .execute()
    )
    return result.data[0] if result.data else None


@app.post("/chat")
def chat(
    req: ChatRequest,
    request: Request,
    _: None = Depends(verify_token),
    __: None = Depends(require_roles("bride", "groom"))
):
    try:
        user_id = request.state.user["id"]
        question = req.message.lower()

        if any(keyword in question for keyword in STRESS_KEYWORDS):
            breathing = get_random_wellness_content("breathing")
            affirmation = get_random_wellness_content("affirmation")

            reply_parts = []

            if affirmation:
                reply_parts.append(affirmation["content"])

            if breathing:
                reply_parts.append(
                    f"\n\nTry this breathing exercise:\n"
                    f"{breathing['title']} — {breathing['content']}"
                )

            reply = "\n".join(reply_parts) or "Take a deep breath. You've got this."

            save_message(user_id, "user", req.message)
            save_message(user_id, "assistant", reply)
            return {"reply": reply}

        if "checklist" in question and "create" in question:
            user = (
                supabase.table("users")
                .select("style,budget,guest_count,wedding_date")
                .eq("id", user_id)
                .single()
                .execute()
                .data
            )
            count = create_ai_checklist(user_id, user)
            reply = f"I’ve created your wedding checklist with {count} tasks."
            save_message(user_id, "user", req.message)
            save_message(user_id, "assistant", reply)
            return {"reply": reply}

    
        history = get_conversation(user_id)
        clean_history = [
            m for m in history
            if isinstance(m.get("content"), str)
        ]

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(clean_history)
        messages.append({"role": "user", "content": req.message})

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=messages
        )

        msg = response.choices[0].message
        reply = msg.get("content") or "I’m not sure how to help with that."

        save_message(user_id, "user", req.message)
        save_message(user_id, "assistant", reply)

        return {"reply": reply}

    except Exception as e:
        print("CHAT ERROR:", e)
        return {"reply": "Something went wrong. Please try again."}
