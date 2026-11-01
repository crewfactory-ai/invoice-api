from datetime import UTC, datetime, timedelta
from decimal import Decimal
from uuid import UUID

from payloads import invoice_in

from app.db import repository


def test_create_invoice_assigns_a_uuid(session):
    invoice = repository.create_invoice(session, invoice_in())

    UUID(invoice.id)


def test_create_invoice_stores_the_lines_in_order(session):
    lines = [
        {"description": "First", "quantity": "1", "unit_price": "1.00", "vat_rate": "0.21"},
        {"description": "Second", "quantity": "1", "unit_price": "2.00", "vat_rate": "0.21"},
        {"description": "Third", "quantity": "1", "unit_price": "3.00", "vat_rate": "0.21"},
    ]
    invoice = repository.create_invoice(session, invoice_in(lines=lines))
    session.expunge_all()

    stored = repository.get_invoice(session, invoice.id)

    assert [line.description for line in stored.lines] == ["First", "Second", "Third"]
    assert [line.position for line in stored.lines] == [1, 2, 3]


def test_create_invoice_keeps_every_decimal_digit(session):
    lines = [
        {"description": "Bolts", "quantity": "1.125", "unit_price": "0.10", "vat_rate": "0.21"}
    ]
    invoice = repository.create_invoice(session, invoice_in(lines=lines))
    session.expunge_all()

    line = repository.get_invoice(session, invoice.id).lines[0]

    assert (line.quantity, line.unit_price, line.vat_rate) == (
        Decimal("1.125"),
        Decimal("0.10"),
        Decimal("0.21"),
    )


def test_create_invoice_stores_the_status(session):
    invoice = repository.create_invoice(session, invoice_in(status="paid"))
    session.expunge_all()

    assert repository.get_invoice(session, invoice.id).status == "paid"


def test_create_invoice_stores_the_currency(session):
    invoice = repository.create_invoice(session, invoice_in(currency="NOK"))
    session.expunge_all()

    assert repository.get_invoice(session, invoice.id).currency == "NOK"


def test_a_missing_cust_ref_is_stored_as_null(session):
    invoice = repository.create_invoice(session, invoice_in(cust_ref=None))
    session.expunge_all()

    assert repository.get_invoice(session, invoice.id).cust_ref is None


def test_get_invoice_returns_the_stored_invoice(session):
    invoice = repository.create_invoice(session, invoice_in(customer_name="Fjord Foods"))
    session.expunge_all()

    stored = repository.get_invoice(session, invoice.id)

    assert stored.customer_name == "Fjord Foods"
    assert str(stored.issue_date) == "2026-10-01"


def test_get_an_unknown_invoice_returns_none(session):
    assert repository.get_invoice(session, "00000000-0000-0000-0000-000000000000") is None


def test_list_invoices_counts_every_invoice(session):
    for _ in range(4):
        repository.create_invoice(session, invoice_in())

    page, total = repository.list_invoices(session, offset=0, limit=2)

    assert (len(page), total) == (2, 4)


def test_list_invoices_orders_by_creation(session):
    start = datetime(2026, 10, 1, 9, 0, tzinfo=UTC)
    for minutes, name in [(2, "Third"), (0, "First"), (1, "Second")]:
        repository.create_invoice(
            session, invoice_in(customer_name=name), now=start + timedelta(minutes=minutes)
        )

    page, _ = repository.list_invoices(session, offset=0, limit=10)

    assert [invoice.customer_name for invoice in page] == ["First", "Second", "Third"]


def test_list_invoices_past_the_end_is_empty(session):
    repository.create_invoice(session, invoice_in())

    page, total = repository.list_invoices(session, offset=5, limit=10)

    assert (page, total) == ([], 1)
