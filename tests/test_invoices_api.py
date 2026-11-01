from uuid import UUID

from payloads import invoice_payload


def test_create_invoice_returns_201_with_an_id(client):
    response = client.post("/v1/invoices", json=invoice_payload())

    assert response.status_code == 201
    UUID(response.json()["id"])


def test_create_invoice_defaults_status_to_draft(client):
    body = client.post("/v1/invoices", json=invoice_payload()).json()

    assert body["status"] == "draft"


def test_create_invoice_keeps_the_given_status(client):
    body = client.post("/v1/invoices", json=invoice_payload(status="issued")).json()

    assert body["status"] == "issued"


def test_create_invoice_defaults_currency_to_eur(client):
    body = client.post("/v1/invoices", json=invoice_payload()).json()

    assert body["currency"] == "EUR"


def test_create_invoice_keeps_the_given_currency(client):
    body = client.post("/v1/invoices", json=invoice_payload(currency="SEK")).json()

    assert body["currency"] == "SEK"


def test_create_invoice_with_a_four_letter_currency_is_400(client):
    response = client.post("/v1/invoices", json=invoice_payload(currency="EURO"))

    assert response.status_code == 400


def test_cust_ref_is_optional(client):
    payload = invoice_payload()
    del payload["cust_ref"]

    body = client.post("/v1/invoices", json=payload).json()

    assert body["cust_ref"] is None


def test_create_invoice_computes_each_line_net(client):
    lines = [{"description": "Paper", "quantity": "3", "unit_price": "19.99", "vat_rate": "0.21"}]

    body = client.post("/v1/invoices", json=invoice_payload(lines=lines)).json()

    assert body["lines"][0]["net"] == "59.97"


def test_create_invoice_computes_the_totals(client):
    lines = [
        {"description": "Consulting", "quantity": "1", "unit_price": "100.00", "vat_rate": "0.21"},
        {"description": "Books", "quantity": "2", "unit_price": "20.00", "vat_rate": "0.09"},
    ]

    body = client.post("/v1/invoices", json=invoice_payload(lines=lines)).json()

    assert (body["net"], body["vat"], body["gross"]) == ("140.00", "24.60", "164.60")


def test_create_invoice_without_lines_is_400(client):
    response = client.post("/v1/invoices", json=invoice_payload(lines=[]))

    assert response.status_code == 400


def test_create_invoice_with_an_empty_customer_name_is_400(client):
    response = client.post("/v1/invoices", json=invoice_payload(customer_name=""))

    assert response.status_code == 400


def test_create_invoice_with_a_negative_unit_price_is_400(client):
    lines = [{"description": "Refund", "quantity": "1", "unit_price": "-5.00", "vat_rate": "0.21"}]

    response = client.post("/v1/invoices", json=invoice_payload(lines=lines))

    assert response.status_code == 400


def test_create_invoice_with_a_zero_quantity_is_400(client):
    lines = [{"description": "Nothing", "quantity": "0", "unit_price": "5.00", "vat_rate": "0.21"}]

    response = client.post("/v1/invoices", json=invoice_payload(lines=lines))

    assert response.status_code == 400


def test_create_invoice_with_a_vat_rate_above_one_is_400(client):
    lines = [{"description": "Typo", "quantity": "1", "unit_price": "5.00", "vat_rate": "21"}]

    response = client.post("/v1/invoices", json=invoice_payload(lines=lines))

    assert response.status_code == 400


def test_create_invoice_with_an_unknown_status_is_400(client):
    response = client.post("/v1/invoices", json=invoice_payload(status="sent"))

    assert response.status_code == 400


def test_a_validation_error_has_a_code_and_the_errors(client):
    body = client.post("/v1/invoices", json=invoice_payload(lines=[])).json()

    assert body["code"] == "invalid_request"
    assert body["errors"][0]["loc"] == ["body", "lines"]


def test_get_invoice_returns_the_created_invoice(client):
    created = client.post("/v1/invoices", json=invoice_payload()).json()

    response = client.get(f"/v1/invoices/{created['id']}")

    assert response.status_code == 200
    assert response.json() == created


def test_get_an_unknown_invoice_is_404_with_a_code(client):
    response = client.get("/v1/invoices/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404
    assert response.json()["code"] == "invoice_not_found"


def test_get_an_invoice_with_a_malformed_id_is_400(client):
    response = client.get("/v1/invoices/not-a-uuid")

    assert response.status_code == 400


def test_the_invoice_list_is_empty_at_first(client):
    body = client.get("/v1/invoices").json()

    assert body == {"items": [], "offset": 0, "limit": 20, "total": 0}


def test_the_invoice_list_pages_with_offset_and_limit(client):
    ids = {client.post("/v1/invoices", json=invoice_payload()).json()["id"] for _ in range(5)}

    first = client.get("/v1/invoices", params={"limit": 3}).json()
    second = client.get("/v1/invoices", params={"offset": 3, "limit": 3}).json()

    assert (len(first["items"]), len(second["items"])) == (3, 2)
    assert {item["id"] for item in first["items"] + second["items"]} == ids
    assert first["total"] == second["total"] == 5


def test_an_invoice_list_limit_above_100_is_400(client):
    response = client.get("/v1/invoices", params={"limit": 101})

    assert response.status_code == 400


def test_a_negative_invoice_list_offset_is_400(client):
    response = client.get("/v1/invoices", params={"offset": -1})

    assert response.status_code == 400
