import logging
import re


def request_log(caplog) -> list[str]:
    return [r.getMessage() for r in caplog.records if r.name == "invoice_api.requests"]


def test_each_request_is_logged_with_method_path_and_status(client, caplog):
    caplog.set_level(logging.INFO, logger="invoice_api.requests")

    client.get("/healthz")

    assert re.fullmatch(r"GET /healthz 200 \d+\.\dms request_id=\w+", request_log(caplog)[0])


def test_the_callers_request_id_is_logged(client, caplog):
    caplog.set_level(logging.INFO, logger="invoice_api.requests")

    client.get("/healthz", headers={"X-Request-Id": "trace-4711"})

    assert request_log(caplog)[0].endswith("request_id=trace-4711")


def test_a_request_without_an_id_gets_a_new_one(client, caplog):
    caplog.set_level(logging.INFO, logger="invoice_api.requests")

    client.get("/healthz")
    client.get("/healthz")

    first, second = (line.rsplit("request_id=", 1)[1] for line in request_log(caplog))
    assert re.fullmatch(r"[0-9a-f]{32}", first)
    assert first != second
