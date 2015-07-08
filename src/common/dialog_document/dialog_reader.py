import csv
import logging
from common.util import list as lu

__author__ = 'Stefan Hillmann'


class DialogsReader:

    """
    Constructor method.
    """
    def __init__(self, filename):
        self.logger = logging.getLogger('dialogs.DialogsReader')
        self.logger.info("Start reading file: %s", filename)

        data_file = open(filename, 'r')
        data_reader = csv.DictReader(data_file, delimiter=';')

        self.data = []
        for row in data_reader:
            self.data.append(row)

        data_file.close()

    def get_rows(self, column, value):

        filtered_rows = []
        for row in self.data:
            if row[column] == value:
                filtered_rows.append(row)
        return filtered_rows

    def get_values(self, column_name):
        values = []
        for row in self.data:
            values.append(row[column_name])

        return values

    def get_unique_values(self, column_name):
        values = self.get_values(column_name)
        return lu.unique_values(values)