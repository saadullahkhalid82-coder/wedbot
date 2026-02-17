from __future__ import annotations
from typing import Optional
import os
from dotenv import load_dotenv
import openai

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise RuntimeError("OPENAI_API_KEY not found in environment")


def generate_wedding_content(
    *,
    content_type: str,
    tone: str,
    couple_names: Optional[str] = None,
    extra_context: Optional[str] = None,
) -> str:
    """
    Generate wedding-related content using AI.
    """

    prompt = f"""
You are a professional wedding writer.

Content type: {content_type}
Tone: {tone}

Couple names: {couple_names or "Not specified"}
Additional context: {extra_context or "None"}

Rules:
- Keep content appropriate for a wedding
- Do NOT invent personal facts
- Keep it warm, natural, and editable
- Length: 2–4 paragraphs
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You write tasteful, wedding-appropriate content."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.6,
    )

    return response.choices[0].message["content"]
