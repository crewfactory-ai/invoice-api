import csv
import io

from payloads import invoice_payload


def rows(client) -> list[list[str]]:
    response = client.get("/v1/exports/invoices.csv")
    return list(csv.reader(io.StringIO(response.text)))


def test_the_export_is_a_csv_attachment(client):
    response = client.get("/v1/exports/invoices.csv")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/csv")
    assert response.headers["content-disposition"] == 'attachment; filename="invoices.csv"'


def test_an_empty_export_has_only_the_header(client):
    assert rows(client) == [
        [
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
    ]


def test_the_export_has_one_row_for_each_invoice(client):
    for _ in range(3):
        client.post("/v1/invoices", json=invoice_payload())

    assert len(rows(client)) == 1 + 3


def test_an_export_row_holds_the_invoice_and_its_totals(client):
    created = client.post("/v1/invoices", json=invoice_payload(cust_ref=None)).json()

    row = rows(client)[1]

    assert row == [
        created["id"],
        "Harbor Supplies",
        "",
        "draft",
        "2026-10-01",
        "2026-10-31",
        "300.00",
        "63.00",
        "363.00",
    ]
