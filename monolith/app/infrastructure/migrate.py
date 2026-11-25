import pathlib

from app.infrastructure.config import Settings
from app.infrastructure.db import connect

MIGRATIONS_DIR = pathlib.Path(__file__).parent / "migrations"


def run(settings=None):
    settings = settings or Settings()
    conn = connect(settings)
    try:
        with conn, conn.cursor() as cur:
            cur.execute("CREATE TABLE IF NOT EXISTS schema_migrations (version TEXT PRIMARY KEY)")
            cur.execute("SELECT version FROM schema_migrations")
            applied = {row[0] for row in cur.fetchall()}
            for path in sorted(MIGRATIONS_DIR.glob("*.sql")):
                if path.name in applied:
                    continue
                cur.execute(path.read_text(encoding="utf-8"))
                cur.execute("INSERT INTO schema_migrations (version) VALUES (%s)", (path.name,))
                print(f"applied {path.name}", flush=True)
    finally:
        conn.close()


if __name__ == "__main__":
    run()
