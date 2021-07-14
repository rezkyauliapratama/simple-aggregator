from src.utils import plugins

usecases = plugins.names_factory(__package__)
execute = plugins.call_factory(__package__)