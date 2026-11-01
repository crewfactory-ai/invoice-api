import re

from sqlalchemy import create_engine, inspect

from app.db.migrate import MIGRATIONS_DIR, apply_migrations


def test_migrations_create_the_tables():
    engine = create_engine("sqlite://")
    apply_migrations(engine)

    assert {"invoices", "invoice_lines"} <= set(inspect(engine).get_table_names())


def test_migrations_apply_only_once(engine):
    assert apply_migrations(engine) == []


def test_migration_files_are_numbered_in_sequence():
    names = sorted(path.name for path in MIGRATIONS_DIR.glob("*.sql"))

    numbers = [int(re.fullmatch(r"(\d{4})_[a-z0-9_]+\.sql", name).group(1)) for name in names]

    assert numbers == list(range(1, len(names) + 1))
