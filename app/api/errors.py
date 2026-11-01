"""Error responses. Every error body has a `code` and a `message`."""

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class InvoiceNotFoundError(Exception):
    def __init__(self, invoice_id: str) -> None:
        super().__init__(invoice_id)
        self.invoice_id = invoice_id


def install(app: FastAPI) -> None:
    app.add_exception_handler(InvoiceNotFoundError, invoice_not_found)
    app.add_exception_handler(RequestValidationError, invalid_request)


async def invoice_not_found(request: Request, exc: InvoiceNotFoundError) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={
            "code": "invoice_not_found",
            "message": f"No invoice has the id {exc.invoice_id}.",
        },
    )


async def invalid_request(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={
            "code": "invalid_request",
            "message": "The request is not valid.",
            "errors": jsonable_encoder(exc.errors()),
        },
    )
