import json
from typing import Any, Dict

from openai import OpenAI
from app.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def extract_order_from_email(email_text: str) -> Dict[str, Any]:
    system_prompt = (
        "You are an assistant that extracts structured data from order confirmation emails. "
        "You ALWAYS respond with ONLY valid JSON, no extra text.\n\n"
        "Fields:\n"
        "- store: string, e.g. 'Amazon'\n"
        "- order_id: string\n"
        "- order_date: ISO format string 'YYYY-MM-DD' if possible\n"
        "- delivery_date: ISO 'YYYY-MM-DD' if present, else null\n"
        "- currency: string like 'USD' if you can infer it, else null\n"
        "- order_total: number if present, else null\n"
        "- items: list of objects { name, price, quantity }\n"
        "- explicit_return_deadline: ISO 'YYYY-MM-DD' if a specific deadline date is given, else null\n"
        "- relative_return_policy_text: short text like '30 days from delivery' if mentioned, else null\n"
    )

    user_prompt = (
        "Extract the fields from the following email. Use null for missing fields.\n\n"
        "EMAIL START\n"
        f"{email_text}\n"
        "EMAIL END\n\n"
        "Respond with ONLY JSON, no explanation."
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.0,
    )

    content = response.choices[0].message.content

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        raise ValueError(f"LLM response was not valid JSON:\n{content}")

    return data
