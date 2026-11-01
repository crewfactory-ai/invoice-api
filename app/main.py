from fastapi import FastAPI

from app.api import errors, invoices

app = FastAPI(title="invoice-api", version="0.1.0")
errors.install(app)
app.include_router(invoices.router)


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}
