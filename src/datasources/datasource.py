from src.datasources.datasource_factory import DatasourceFactory


class Datasource:
    def __init__(self, factory: DatasourceFactory):
        self._factory = factory
        self._datasource = factory.make_datasource()

    def get_datasource(self) -> any:
        return self._datasource
