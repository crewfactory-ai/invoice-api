from fastapi import FastAPI

from app.api import errors, exports, invoices
from app.middleware import RequestLogMiddleware

app = FastAPI(title="invoice-api", version="0.3.0")
app.add_middleware(RequestLogMiddleware)
errors.install(app)
app.include_router(invoices.router)
app.include_router(exports.router)


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}
