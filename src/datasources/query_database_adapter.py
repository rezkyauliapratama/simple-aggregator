import logging
from typing import List, Optional, Union

from sqlalchemy import text
from sqlalchemy.engine import Engine

from src.datasources.datasource import Datasource
from src.datasources.datasource_factory import PgDatasourceFactory
from src.utils.log_helper import LogHelper


class QueryProcessorAdapter:
    logger = logging.getLogger(__name__)

    def __init__(self, query: str, factory: PgDatasourceFactory):
        self.query = query
        self.factory = factory

    def get_result_data(self, func=None) -> Optional[Union[list, dict, List[dict]]]:
        datasource: Engine = Datasource(factory=self.factory).get_datasource()
        sql = text(
            self.query
        )

        print(sql)
        LogHelper.log(__name__, f"[Query] {sql}", logging.DEBUG)

        result = datasource.execute(
            sql
        )

        LogHelper.log(__name__, f"[Query Result] rows={result.rowcount}", logging.INFO)

        if result.rowcount == 0:
            return None

        result_dicts = [dict(row) for row in result]
        if func is None:
            return result_dicts

        result_transform_dicts = func(result_dicts)
        return result_transform_dicts
