# services/vendor_comparison_ai.py

from __future__ import annotations

from typing import List, Dict
import os

from dotenv import load_dotenv
import openai

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise RuntimeError(
        "OPENAI_API_KEY not found. Check your .env file and restart the terminal."
    )


def generate_vendor_comparison(
    vendors: List[Dict],
    *,
    budget: int,
    category: str,
) -> str:
    """
    Generate a natural-language comparison of vendors.
    """

    if not vendors:
        return "No vendors available to compare."

    vendor_lines = []
    for v in vendors:
        vendor_lines.append(
            f"- {v['name']} | "
            f"City: {v['city']} | "
            f"Price: {v['recommended_price']} | "
            f"Style: {', '.join(v['style_tags'])}"
        )

    vendor_block = "\n".join(vendor_lines)

    prompt = f"""
You are a wedding planning assistant.

The user is looking for {category} under a budget of {budget}.

Here are the vendor options:
{vendor_block}

Write a concise, friendly comparison (3–5 sentences):
- Highlight strengths of each vendor
- Mention style differences
- Keep tone professional and helpful
- Do NOT invent prices or features
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful wedding planning assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.4,
    )

    return response.choices[0].message["content"]
