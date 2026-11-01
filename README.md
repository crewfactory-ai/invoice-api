# invoice-api

A small REST service for issuing and listing invoices.

## Run

```sh
python3.14 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Test

```sh
python -m pytest -q
ruff check .
```
