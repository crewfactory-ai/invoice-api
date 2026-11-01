# 0002. FastAPI, SQLAlchemy and SQLite

- Status: accepted
- Date: 2026-11-01

## Context

The service is small, has one team and must be easy to run on a laptop.

## Decision

- The HTTP layer is FastAPI with Pydantic models for every request and response body.
- Persistence is SQLAlchemy 2 in the ORM style, behind the functions of `app/db/repository.py`.
  Route handlers do not build queries.
- The database is SQLite. Tests use an in-memory database.
- Dependencies are pinned to exact versions in `requirements.txt`. A new dependency needs a
  reason in its pull request.

## Consequences

Moving to another database later means changing the engine URL and checking the migrations.
