import os


class Settings:
    def __init__(self, env=None):
        env = os.environ if env is None else env
        self.port = int(env.get("PORT", "8081"))
        self.repo_adapter = env.get("REPO_ADAPTER", "db").lower()
        self.db_host = env.get("DB_HOST", "db")
        self.db_port = int(env.get("DB_PORT", "5432"))
        self.db_name = env.get("DB_NAME", "orders")
        self.db_user = env.get("DB_USER", "orders")
        self.db_pass = env.get("DB_PASS", "orders")
        self.csv_path = env.get("CSV_PATH", "/data/orders.csv")
