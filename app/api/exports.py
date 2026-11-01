import csv
import io

from fastapi import APIRouter
from fastapi.responses import Response

from app.api.deps import SessionDep
from app.db import repository
from app.domain.tax import invoice_totals

router = APIRouter(prefix="/v1/exports", tags=["exports"])

COLUMNS = [
    "id",
    "customer_name",
    "cust_ref",
    "status",
    "issue_date",
    "due_date",
    "net",
    "vat",
    "gross",
]


@router.get(
    "/invoices.csv",
    response_class=Response,
    responses={200: {"content": {"text/csv": {}}}},
)
def export_invoices(session: SessionDep) -> Response:
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(COLUMNS)
    for invoice in repository.iter_invoices(session):
        totals = invoice_totals(invoice.lines)
        writer.writerow(
            [
                invoice.id,
                invoice.customer_name,
                invoice.cust_ref or "",
                invoice.status,
                invoice.issue_date.isoformat(),
                invoice.due_date.isoformat(),
                totals.net,
                totals.vat,
                totals.gross,
            ]
        )
    return Response(
        buffer.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="invoices.csv"'},
    )
