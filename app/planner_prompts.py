CHECKLIST_PROMPT = """
Generate a wedding checklist with 50–80 tasks.
Context:
- Wedding type: {style}
- Budget: {budget}
- Guests: {guests}
- Wedding date: {date}

Return ONLY a JSON array of task strings.
"""
