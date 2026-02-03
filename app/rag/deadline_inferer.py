from __future__ import annotations

import re
from datetime import date, timedelta
from typing import Optional, Tuple


def infer_deadline(
    explicit_deadline: Optional[date],
    delivery_date: Optional[date],
    relative_policy_text: Optional[str],
) -> Tuple[Optional[date], Optional[str]]:
    """
    Returns (deadline_date, source)
    source in {"EXPLICIT", "RELATIVE", None}
    """
    if explicit_deadline:
        return explicit_deadline, "EXPLICIT"

    if delivery_date and relative_policy_text:
        t = relative_policy_text.lower()

        # Simple pattern: "30 days" or "within 30 days"
        m = re.search(r"(\d{1,3})\s*days", t)
        if m:
            days = int(m.group(1))
            return delivery_date + timedelta(days=days), "RELATIVE"

    return None, None
