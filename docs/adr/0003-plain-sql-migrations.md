# 0003. Plain SQL migrations

- Status: accepted
- Date: 2026-11-01

## Context

The schema is small and changes a few times a year. A migration framework would be the largest
dependency of the service.

## Decision

- Each schema change is one SQL file in `migrations/`, named `NNNN_what_it_does.sql`, numbered
  in sequence with no gaps.
- `app/db/migrate.py` applies the files in name order and records each applied file in the table
  `schema_migrations`. A file is applied once.
- An applied file is never edited. A correction is a new file.
- The SQLAlchemy models in `app/db/models.py` follow the migrations. The tests build their
  database from the migrations, so a model column with no migration fails the suite.

## Consequences

There are no down migrations. A change that must be undone is undone by a new file.
