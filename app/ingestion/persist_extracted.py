from __future__ import annotations

from datetime import date
from typing import Any, Dict, Optional

from sqlalchemy import select

from app.db.base import SessionLocal
from app.db.models import Order, OrderItem


def _parse_date(s: Optional[str]) -> Optional[date]:
    if not s:
        return None
    # expects YYYY-MM-DD from your LLM output
    return date.fromisoformat(s)


def upsert_order(extracted: Dict[str, Any]) -> int:
    """
    Upserts an order by external order id and replaces items.
    Returns the DB order.id.
    """
    store = extracted.get("store") or "Unknown"
    order_id_external = extracted.get("order_id")
    if not order_id_external:
        raise ValueError("Missing order_id in extracted payload")

    with SessionLocal() as session:
        existing = session.execute(
            select(Order).where(Order.order_id_external == order_id_external)
        ).scalar_one_or_none()

        if existing is None:
            order = Order(store=store, order_id_external=order_id_external)
            session.add(order)
            session.flush()
        else:
            order = existing
            # clear items (we’ll re-add)
            order.items.clear()

        order.order_date = _parse_date(extracted.get("order_date"))
        order.delivery_date = _parse_date(extracted.get("delivery_date"))
        order.currency = extracted.get("currency")
        order.order_total = extracted.get("order_total")
        order.explicit_return_deadline = _parse_date(extracted.get("explicit_return_deadline"))
        order.relative_return_policy_text = extracted.get("relative_return_policy_text")
        from app.rag.deadline_inferer import infer_deadline

        final_deadline, source = infer_deadline(
        explicit_deadline=order.explicit_return_deadline,
        delivery_date=order.delivery_date,
        relative_policy_text=order.relative_return_policy_text,
        )
        order.final_return_deadline = final_deadline
        order.return_deadline_source = source

        items = extracted.get("items") or []
        for it in items:
            order.items.append(
                OrderItem(
                    name=it.get("name") or "Unknown item",
                    price=it.get("price"),
                    quantity=int(it.get("quantity") or 1),
                )
            )

        session.commit()
        return order.id
