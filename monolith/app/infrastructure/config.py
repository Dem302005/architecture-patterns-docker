import os


class Settings:
    def __init__(self):
        self.db_host = os.getenv("DB_HOST", "db")
        self.db_port = int(os.getenv("DB_PORT", "5432"))
        self.db_name = os.getenv("DB_NAME", "shop")
        self.db_user = os.getenv("DB_USER", "shop")
        self.db_pass = os.getenv("DB_PASS", "shop")
        self.port = int(os.getenv("PORT", "8080"))
        self.redis_host = os.getenv("REDIS_HOST", "")
        self.redis_port = int(os.getenv("REDIS_PORT", "6379"))
        self.cache_ttl = int(os.getenv("CACHE_TTL", "30"))
