import csv
import io
import logging
from typing import List

from src.domain.interfaces.io_interface import IOInterface
from src.utils.log_helper import LogHelper


class CsvAdapter(IOInterface):

    def __init__(self, data_dicts: List[dict]):
        """
            Initial function
            :param data_dicts: the list of header name
        """
        self.writer_io = io.StringIO()
        self.data_dicts = data_dicts

    def convert(self, header_uppercase: bool = False, delimiter: str = ',', exclude_keys=None):
        """
            The function to convert data into IO
            :param header_uppercase: default False, set true if you want to convert the header column to uppercase
            :param delimiter: the delimeters that will be used in csv
            :param exclude_keys: the list of keys that will be excluded from csv
            :return WriterIO
            :rtype io
        """

        if exclude_keys is None:
            exclude_keys = {}

        if self.data_dicts is None or len(self.data_dicts) < 1:
            return None

        LogHelper.log(__name__, f"Total data that will be transformed is {len(self.data_dicts)}",
                      logging.DEBUG)
        LogHelper.log(__name__,
                      f"uppercase [{header_uppercase}], delimiter [{delimiter}], exclude_keys [{exclude_keys}]",
                      logging.DEBUG)

        if header_uppercase:
            transform_dicts = [{str(key).upper(): value for key, value in e.items() if key not in exclude_keys}
                               for e in
                               self.data_dicts]
        else:
            transform_dicts = [{str(key).lower(): value for key, value in e.items() if key not in exclude_keys}
                               for e in
                               self.data_dicts]

        writer = csv.DictWriter(self.writer_io, delimiter=delimiter, fieldnames=transform_dicts[0].keys())
        writer.writeheader()

        for row in transform_dicts:
            writer.writerow(row)

        LogHelper.log(__name__, f"All data successfully transformed", logging.DEBUG)

        return self.writer_io
