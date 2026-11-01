# invoice-api

A small REST service for issuing and listing invoices, with VAT, CSV export and request tracing.

This repository is a sample codebase for demonstrating AI-assisted software delivery: work arrives
as issues and leaves as reviewed pull requests.

## Run

```sh
python3.14 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python -m app.db.migrate
uvicorn app.main:app --reload
```

The database is `invoices.db` in the working directory. Set `DATABASE_URL` to use another one.
The API documentation is at <http://127.0.0.1:8000/docs>.

## Test and lint

```sh
python -m pytest -q
ruff check .
```

CI runs both on each pull request and on each push to `master`.

## Endpoints

| Method | Path | Answer |
| --- | --- | --- |
| `POST` | `/v1/invoices` | `201` with the created invoice and its totals |
| `GET` | `/v1/invoices` | One page of invoices: `offset` (default 0) and `limit` (default 20, at most 100) |
| `GET` | `/v1/invoices/{invoice_id}` | The invoice, or `404` with the code `invoice_not_found` |
| `GET` | `/v1/exports/invoices.csv` | Every invoice as CSV |
| `GET` | `/healthz` | `{"status": "ok"}` |

## Layout

| Path | Content |
| --- | --- |
| `app/main.py` | The application: middleware, error handlers, routers |
| `app/api/` | Route handlers (`invoices.py`, `exports.py`) and the error responses (`errors.py`) |
| `app/schemas.py` | Request and response models |
| `app/domain/tax.py` | Line and invoice totals, VAT |
| `app/db/` | Models, the repository and the migration runner |
| `app/middleware.py` | Request logging |
| `migrations/` | The schema, one numbered SQL file for each change |
| `docs/adr/` | Decision records |

## Conventions

- Every error body has a `code` and a `message`. A request that fails validation answers `400`
  with the code `invalid_request`.
- Money is `Decimal` and travels as a string, for example `"10.50"`. VAT is rounded as
  [ADR 0004](docs/adr/0004-vat-rounding.md) decides.
- A schema change is a new numbered file in `migrations/`. An applied file is never edited
  ([ADR 0003](docs/adr/0003-plain-sql-migrations.md)).
- Only `app/db/repository.py` queries the database.
- Each change comes with tests. A new dependency needs a reason in its pull request.
