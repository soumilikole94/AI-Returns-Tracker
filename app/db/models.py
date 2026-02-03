from __future__ import annotations

from datetime import date
from typing import Optional

from sqlalchemy import Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    store: Mapped[str] = mapped_column(String, nullable=False)
    order_id_external: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    order_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    delivery_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    currency: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    order_total: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    explicit_return_deadline: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    relative_return_policy_text: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    final_return_deadline: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    return_deadline_source: Mapped[Optional[str]] = mapped_column(String, nullable=True)  # EXPLICIT / RELATIVE / RAG

    items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order", cascade="all, delete-orphan"
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)

    name: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    order: Mapped["Order"] = relationship(back_populates="items")
