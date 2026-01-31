from typing import Any, Dict
from app.models.llm_client import extract_order_from_email


def parse_email_to_order(email_text: str) -> Dict[str, Any]:
    # TODO: add PII redaction here later before sending to the LLM
    return extract_order_from_email(email_text)
