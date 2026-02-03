from __future__ import annotations

from sqlalchemy import select

from app.db.base import SessionLocal
from app.db.models import Order


def main():
    with SessionLocal() as session:
        orders = session.execute(select(Order).order_by(Order.id)).scalars().all()

        if not orders:
            print("No orders found.")
            return

        print(f"Found {len(orders)} orders:\n")

        for o in orders:
            print("=" * 80)
            print(f"DB id: {o.id}")
            print(f"Store: {o.store}")
            print(f"External order id: {o.order_id_external}")
            print(f"Order date: {o.order_date}")
            print(f"Delivery date: {o.delivery_date}")
            print(f"Currency: {o.currency}")
            print(f"Order total: {o.order_total}")
            print(f"Explicit return deadline: {o.explicit_return_deadline}")
            print(f"Relative return policy text: {o.relative_return_policy_text}")
            print(f"Final return deadline: {o.final_return_deadline} (source={o.return_deadline_source})")
            print("Items:")
            for it in o.items:
                print(f"  - {it.name} | price={it.price} | qty={it.quantity}")
            print()

if __name__ == "__main__":
    main()
