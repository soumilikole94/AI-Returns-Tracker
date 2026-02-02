from __future__ import annotations

import re
from typing import Literal

EmailType = Literal["ORDER_CONFIRMATION", "SHIPPING", "DELIVERY", "OTHER"]


def classify_email(raw_text: str) -> EmailType:
    """
    Lightweight heuristic classifier.
    Good enough for v1; later we can swap to LLM or a small supervised model.
    """
    t = raw_text.lower()

    # Very common Amazon patterns
    if "has been placed" in t or "we have received your order" in t or "order confirmation" in t:
        return "ORDER_CONFIRMATION"

    if "has shipped" in t or "track your shipment" in t or "items in this shipment" in t:
        return "SHIPPING"

    if "was delivered" in t or "package was delivered" in t or "delivered:" in t:
        return "DELIVERY"

    # fallback
    return "OTHER"
