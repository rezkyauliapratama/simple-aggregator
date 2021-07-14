import os

from dependency_injector import providers, containers

from datasources.datasource_factory import PgDatasourceFactory


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    pg_datasource_factory = providers.Singleton(
        PgDatasourceFactory,
        db_name=os.getenv('DB_NAME', None),
        db_user=os.getenv('DB_USER', None),
        db_pass=os.getenv('DB_PASS', None),
        db_addr=os.getenv('DB_ADDR', None)
    )
