from io import BytesIO
from typing import List
import pandas as pd
from fastapi.responses import StreamingResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from app.db import supabase


def export_tasks_csv(user_id: str) -> StreamingResponse:
    response = (
        supabase
        .table("tasks")
        .select("title,status,created_at")
        .eq("user_id", user_id)
        .execute()
    )

    df = pd.DataFrame(response.data)

    buffer = BytesIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=tasks.csv"
        }
    )

def export_budget_pdf(user_id: str) -> StreamingResponse:
    response = (
        supabase
        .table("budget_categories")
        .select("category,allocated,spent")
        .eq("user_id", user_id)
        .execute()
    )

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(40, height - 40, "Wedding Budget Breakdown")

    y = height - 80
    pdf.setFont("Helvetica", 11)

    for row in response.data:
        pdf.drawString(
            40,
            y,
            f"{row['category']}: Allocated {row['allocated']} | Spent {row['spent']}"
        )
        y -= 20

        if y < 40:
            pdf.showPage()
            y = height - 40

    pdf.save()
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=budget.pdf"
        }
    )


def export_checklist_pdf(user_id: str) -> StreamingResponse:
    response = (
        supabase
        .table("tasks")
        .select("title,status")
        .eq("user_id", user_id)
        .execute()
    )

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(40, height - 40, "Wedding Checklist")

    y = height - 80
    pdf.setFont("Helvetica", 11)

    for task in response.data:
        status = "✓" if task["status"] == "completed" else "☐"
        pdf.drawString(40, y, f"{status} {task['title']}")
        y -= 18

        if y < 40:
            pdf.showPage()
            y = height - 40

    pdf.save()
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=checklist.pdf"
        }
    )
