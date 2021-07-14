# The Abstract Factory:
import abc

from sqlalchemy import create_engine

from src.utils.log_helper import LogHelper


class DatasourceFactory(abc.ABC):
    @abc.abstractmethod
    def make_datasource(self): pass


class PgDatasourceFactory(DatasourceFactory):
    DATABASE_URI = "postgres://{DB_USER}:{DB_PASS}@{DB_ADDR}:{DB_PORT}/{DB_NAME}"

    def __init__(self, db_name: str, db_user: str, db_pass: str, db_addr: str, db_port, **kwargs):
        self.host_url = self.DATABASE_URI.format(
            DB_USER=db_user,
            DB_PASS=db_pass,
            DB_ADDR=db_addr,
            DB_PORT=db_port,
            DB_NAME=db_name
        )

        LogHelper.log(__name__, f"host_url : {self.host_url}")
        self.kwargs = kwargs

    def make_datasource(self):
        return create_engine(self.host_url, **self.kwargs)
