from fastapi import FastAPI

from app.api import errors, exports, invoices

app = FastAPI(title="invoice-api", version="0.2.0")
errors.install(app)
app.include_router(invoices.router)
app.include_router(exports.router)


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}
