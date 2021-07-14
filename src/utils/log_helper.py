import logging.config
import sys
import traceback

from jsonformatter import JsonFormatter


class LogHelper:
    STRING_FORMAT = '''{
        "Created":         "created",
        "Asctime":         "asctime",
        "Levelname":       "levelname",
        "Message":         "message"
    }'''

    def __init__(self, level: int = logging.DEBUG):
        self.root = logging.getLogger(__name__)

        if not self.root.hasHandlers():
            formatter = JsonFormatter(self.STRING_FORMAT, indent=4, ensure_ascii=False, mix_extra=True,
                                      mix_extra_position='tail')

            sh = logging.StreamHandler()
            sh.setFormatter(formatter)
            self.root.addHandler(sh)
            self.root.setLevel(level)

    def __log_msg(self, msg: str, level: int = logging.INFO):

        if level == logging.INFO:
            self.root.info(msg)
        elif level == logging.DEBUG:
            self.root.debug(msg)
        elif level == logging.ERROR:
            self.__log_error(msg)

    def __log_error(self, exc):
        exc_type, exc_obj, exc_tb = sys.exc_info()
        list_of_details = []
        for err in traceback.extract_tb(exc_tb):
            if ".venv" not in err[0]:
                list_of_details.append(f"F=%s | L=%s" % (err[0], err[1]))

        if hasattr(exc, 'message'):
            message: str = exc.message
        else:
            message: str = str(exc)

        extra = None
        if len(list_of_details) > 1:
            extra = {"details": list_of_details}

        self.root.error(message, extra=extra)

    @classmethod
    def log(cls, filename: str, message: str, level: int = logging.INFO):
        return cls().__log_msg(f"[%s] %s" % (filename.strip(), message.strip()), level)

    @classmethod
    def log_error(cls, exc):
        return cls().__log_error(exc)
