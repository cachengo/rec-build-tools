# Copyright 2019 Nokia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import re


def to_json(data):
    return json.dumps(data, sort_keys=True, indent=4)


class CsvConverter(object):
    def __init__(self, data, preferred_field_order=None, escape_newlines=True):
        self.data = data
        self.preferred_field_order = preferred_field_order
        self.escape_newlines = escape_newlines
        self.csv_data = None
        self._convert()

    def __str__(self):
        return self.convert()

    def convert(self):
        return self._render(CsvFormatter(self.csv_data))

    def convert_to_ms_excel(self, text_fields=None):
        """
        CSV that Microsoft Excel can read well.

        :param text_fields: list of columns to mark as text
                            NOTE: must not be used for fields that can contain comma(,) or
                            semicolon(;) as field will be split from these
        :return:
        """
        return self._render(CsvMSFormatter(self.csv_data, text_fields=text_fields))

    def _convert(self):
        if not isinstance(self.data, list):
            raise Exception('Input data given is NOT a list')
        if not self.data:
            self.csv_data = []
            return
        if not isinstance(self.data[0], dict):
            raise Exception('First data element is NOT a dict')
        headers = []
        possible_fields = list(set([key for i in self.data for key in i.keys()]))
        if self.preferred_field_order is not None:
            for preferred_field in self.preferred_field_order:
                if preferred_field in possible_fields:
                    headers.append(preferred_field)
                    possible_fields.remove(preferred_field)
        headers += sorted(possible_fields)
        self.csv_data = [headers]
        for obj in self.data:
            row_data = []
            for header in headers:
                field = obj.get(header)
                if isinstance(field, (list, dict)):
                    x = json.dumps(field, sort_keys=True)
                elif isinstance(field, unicode):
                    x = field.encode('utf-8')
                else:
                    x = str(field)
                row_data.append(x)
            self.csv_data.append(row_data)

    def _render(self, formatter):
        return formatter.format(self.escape_newlines)


class CsvFormatter(object):
    def __init__(self, csv_data):
        self.csv_data = csv_data

    def format(self, escape_newlines=True):
        f_file = []
        for record in self.csv_data:
            f_record = []
            for field in record:
                f_field = self._field_formatter(field, escape_newlines)
                f_record.append(f_field)
            f_file.append(','.join(self._record_formatter(f_record)))
        return '\r\n'.join(self._file_formatter(f_file))

    @staticmethod
    def _file_formatter(_file):
        return _file

    @staticmethod
    def _record_formatter(record):
        return ['"{}"'.format(i) for i in record]

    @staticmethod
    def _field_formatter(field, escape_newlines):
        out = field.replace('"', '""')
        if escape_newlines:
            out = out.replace('\n', '\\n')
        return out


class CsvMSFormatter(CsvFormatter):
    max_cell_size = 32000

    def __init__(self, csv_data, text_fields=None):
        super(CsvMSFormatter, self).__init__(csv_data)
        self.text_fields = text_fields

    def _file_formatter(self, _file):
        return ['sep=,'] + super(CsvMSFormatter, self)._file_formatter(_file)

    def _record_formatter(self, record):
        record = super(CsvMSFormatter, self)._record_formatter(record)
        if self.text_fields:
            formatted_record = []
            for index, field in enumerate(record):
                heading = self.csv_data[0][index]
                if heading in self.text_fields:
                    formatted_field = '=' + field
                else:
                    formatted_field = field
                formatted_record.append(formatted_field)
            record = formatted_record
        return record

    def _field_formatter(self, field, escape_newlines):
        field = super(CsvMSFormatter, self)._field_formatter(field, escape_newlines)
        if len(field) > self.max_cell_size:
            field = field[:self.max_cell_size / 2] + "..." + field[-self.max_cell_size / 2:]
        if not re.match(r'^-\d+$', field) and re.match(r'^-.*$', field):
            return r'\{}'.format(field)
        return field
