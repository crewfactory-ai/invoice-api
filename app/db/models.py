from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import ForeignKey, String
from sqlalchemy.engine import Dialect
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.types import TypeDecorator


class DecimalText(TypeDecorator[Decimal]):
    """A Decimal stored as text, so that SQLite keeps every digit."""

    impl = String
    cache_ok = True

    def process_bind_param(self, value: Decimal | None, dialect: Dialect) -> str | None:
        return None if value is None else str(value)

    def process_result_value(self, value: str | None, dialect: Dialect) -> Decimal | None:
        return None if value is None else Decimal(value)


class Base(DeclarativeBase):
    pass


class Invoice(Base):
    __tablename__ = "invoices"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    customer_name: Mapped[str]
    cust_ref: Mapped[str | None]
    status: Mapped[str]
    issue_date: Mapped[date]
    due_date: Mapped[date]
    created_at: Mapped[datetime]
    lines: Mapped[list[InvoiceLine]] = relationship(
        order_by="InvoiceLine.position", cascade="all, delete-orphan", lazy="selectin"
    )


class InvoiceLine(Base):
    __tablename__ = "invoice_lines"

    id: Mapped[int] = mapped_column(primary_key=True)
    invoice_id: Mapped[str] = mapped_column(ForeignKey("invoices.id"))
    position: Mapped[int]
    description: Mapped[str]
    quantity: Mapped[Decimal] = mapped_column(DecimalText)
    unit_price: Mapped[Decimal] = mapped_column(DecimalText)
    vat_rate: Mapped[Decimal] = mapped_column(DecimalText)
