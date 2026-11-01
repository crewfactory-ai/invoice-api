"""The only module that queries the database (ADR 0002)."""

from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.models import Invoice, InvoiceLine
from app.schemas import InvoiceIn


def create_invoice(session: Session, data: InvoiceIn, *, now: datetime | None = None) -> Invoice:
    invoice = Invoice(
        id=str(uuid4()),
        customer_name=data.customer_name,
        cust_ref=data.cust_ref,
        currency=data.currency,
        status=data.status,
        issue_date=data.issue_date,
        due_date=data.due_date,
        created_at=now or datetime.now(UTC),
        lines=[
            InvoiceLine(
                position=position,
                description=line.description,
                quantity=line.quantity,
                unit_price=line.unit_price,
                vat_rate=line.vat_rate,
            )
            for position, line in enumerate(data.lines, start=1)
        ],
    )
    session.add(invoice)
    session.commit()
    return invoice


def get_invoice(session: Session, invoice_id: str) -> Invoice | None:
    return session.get(Invoice, invoice_id)


def list_invoices(session: Session, *, offset: int, limit: int) -> tuple[list[Invoice], int]:
    total = session.scalar(select(func.count()).select_from(Invoice)) or 0
    page = session.scalars(
        select(Invoice).order_by(Invoice.created_at, Invoice.id).offset(offset).limit(limit)
    )
    return list(page), total
