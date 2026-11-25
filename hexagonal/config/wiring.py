from adapters.http.app import create_app
from config.settings import Settings
from core.usecases import CreateOrder, GetOrder


def build_repository(settings):
    if settings.repo_adapter == "file":
        from adapters.file.csv_repository import CsvOrderRepository

        return CsvOrderRepository(settings.csv_path)
    if settings.repo_adapter == "db":
        from adapters.db.postgres_repository import PostgresOrderRepository

        return PostgresOrderRepository(
            settings.db_host, settings.db_port, settings.db_name, settings.db_user, settings.db_pass
        )
    raise ValueError(f"unknown REPO_ADAPTER: {settings.repo_adapter}")


def build_app(settings=None, repository=None):
    settings = settings or Settings()
    repository = repository or build_repository(settings)
    return create_app(CreateOrder(repository), GetOrder(repository))
