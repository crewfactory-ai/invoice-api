"""Apply the SQL files in migrations/ in name order, each one once (ADR 0003)."""

from pathlib import Path

from sqlalchemy import Engine, text

MIGRATIONS_DIR = Path(__file__).resolve().parents[2] / "migrations"


def apply_migrations(engine: Engine) -> list[str]:
    applied: list[str] = []
    with engine.begin() as connection:
        connection.execute(
            text("CREATE TABLE IF NOT EXISTS schema_migrations (name TEXT PRIMARY KEY)")
        )
        done = set(connection.scalars(text("SELECT name FROM schema_migrations")))
        for path in sorted(MIGRATIONS_DIR.glob("*.sql")):
            if path.name in done:
                continue
            for statement in path.read_text().split(";"):
                if statement.strip():
                    connection.execute(text(statement))
            connection.execute(
                text("INSERT INTO schema_migrations (name) VALUES (:name)"), {"name": path.name}
            )
            applied.append(path.name)
    return applied


if __name__ == "__main__":
    from app.db.session import engine

    for name in apply_migrations(engine):
        print(f"applied {name}")
