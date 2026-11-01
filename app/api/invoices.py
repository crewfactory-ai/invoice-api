from uuid import UUID

from fastapi import APIRouter

from app.api.deps import SessionDep
from app.api.errors import InvoiceNotFoundError
from app.db import repository
from app.db.models import Invoice
from app.domain.tax import invoice_totals, line_net
from app.schemas import ErrorOut, InvoiceIn, InvoiceLineOut, InvoiceOut

router = APIRouter(prefix="/v1/invoices", tags=["invoices"])


def to_out(invoice: Invoice) -> InvoiceOut:
    totals = invoice_totals(invoice.lines)
    return InvoiceOut(
        id=UUID(invoice.id),
        customer_name=invoice.customer_name,
        cust_ref=invoice.cust_ref,
        status=invoice.status,
        issue_date=invoice.issue_date,
        due_date=invoice.due_date,
        lines=[
            InvoiceLineOut(
                description=line.description,
                quantity=line.quantity,
                unit_price=line.unit_price,
                vat_rate=line.vat_rate,
                net=line_net(line),
            )
            for line in invoice.lines
        ],
        net=totals.net,
        vat=totals.vat,
        gross=totals.gross,
    )


@router.post("", status_code=201)
def create_invoice(body: InvoiceIn, session: SessionDep) -> InvoiceOut:
    return to_out(repository.create_invoice(session, body))


@router.get("/{invoice_id}", responses={404: {"model": ErrorOut}})
def get_invoice(invoice_id: UUID, session: SessionDep) -> InvoiceOut:
    invoice = repository.get_invoice(session, str(invoice_id))
    if invoice is None:
        raise InvoiceNotFoundError(str(invoice_id))
    return to_out(invoice)
