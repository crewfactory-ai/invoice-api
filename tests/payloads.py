from app.schemas import InvoiceIn


def invoice_payload(**overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "customer_name": "Harbor Supplies",
        "cust_ref": "HS-1042",
        "issue_date": "2026-10-01",
        "due_date": "2026-10-31",
        "lines": [
            {
                "description": "Consulting",
                "quantity": "2",
                "unit_price": "150.00",
                "vat_rate": "0.21",
            }
        ],
    }
    payload.update(overrides)
    return payload


def invoice_in(**overrides: object) -> InvoiceIn:
    return InvoiceIn.model_validate(invoice_payload(**overrides))
