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

# pylint: disable=invalid-name
from collections import OrderedDict

import pytest

from tools.convert import to_json, CsvConverter


class TestJson(object):
    @staticmethod
    def test_json():
        _input = dict(b=1, a=2)
        expected = '\n'.join(['{',
                              '    "a": 2, ',
                              '    "b": 1',
                              '}'])
        assert to_json(_input) == expected


class TestCsv(object):
    @staticmethod
    @pytest.mark.parametrize('_input, expected', [
        ([], ''),
        ([{}], '\r\n'),
        ([dict(a=1)], '\r\n'.join(['"a"',
                                   '"1"'])),
        ([dict(a=1), dict(a=2)], '\r\n'.join(['"a"',
                                              '"1"',
                                              '"2"'])),
        ([dict(a=1, b=2), dict(a=3, b=4)], '\r\n'.join(['"a","b"',
                                                        '"1","2"',
                                                        '"3","4"'])),
        ([dict(x=OrderedDict({'b': 1, 'a': 2})),
          dict(x={'a': 2, 'b': 1})], '\r\n'.join(['"x"',
                                                  '"{""a"": 2, ""b"": 1}"',
                                                  '"{""a"": 2, ""b"": 1}"']))

    ])
    def test_csv(_input, expected):
        assert str(CsvConverter(_input)) == expected

    @staticmethod
    def test_str():
        _input = [dict(a=1)]
        assert str(CsvConverter(_input)) == CsvConverter(_input).convert()

    @staticmethod
    @pytest.mark.parametrize('_input, exception_re', [
        ('boom', r'NOT a list'),
        ([['boom']], r'NOT a dict')
    ])
    def test_to_csv_fail(_input, exception_re):
        with pytest.raises(Exception, match=exception_re):
            str(CsvConverter(_input))

    @staticmethod
    def test_newlines_are_escaped():
        """
        ...in order to get properly formatted file when written
        """
        _input = [dict(a='1"2')]
        expected = '\r\n'.join(['"a"',
                                '"1""2"'])
        assert CsvConverter(_input).convert() == expected

    @staticmethod
    def test_missing_fields_are_filled_with_none():
        _input = [dict(a='1"2')]
        expected = '\r\n'.join(['"a"',
                                '"1""2"'])
        assert CsvConverter(_input).convert() == expected

    @staticmethod
    def test_double_quote_is_escaped_with_double_quote():
        """
        RFC 4180
        """
        _input = [dict(a='1"2')]
        expected = '\r\n'.join(['"a"',
                                '"1""2"'])
        assert CsvConverter(_input).convert() == expected

    @staticmethod
    @pytest.mark.parametrize('_input, expected', [
        ([dict(a=1, b=2)], '\r\n'.join(['"b","a"', '"2","1"'])),
        ([dict(a=1, c=2)], '\r\n'.join(['"a","c"', '"1","2"']))
    ])
    def test_csv_preferred_order(_input, expected):
        assert CsvConverter(_input, preferred_field_order=['b', 'a']).convert() == expected

    @staticmethod
    @pytest.mark.parametrize('_input, expected', [
        ([dict(a='Copyright \xc2\xa9 2014')], '\r\n'.join(['"a"',
                                                           '"Copyright \xc2\xa9 2014"'])),
        ([dict(a=u'Copyright \xa9 2014')], '\r\n'.join(['"a"',
                                                        '"Copyright \xc2\xa9 2014"'])),
    ])
    def test_unicode_input(_input, expected):
        assert str(CsvConverter(_input)) == expected


class TestCsvMSExcel(object):
    @staticmethod
    def test_ms_excel_format():
        """
        MS Excel treats CSV files with 'sep=,' as the first line to get automatically columnized
        """
        _input = [dict(a=1, b=2)]
        expected = '\r\n'.join(['sep=,',
                                '"a","b"',
                                '"1","2"'])
        assert CsvConverter(_input).convert_to_ms_excel() == expected

    @staticmethod
    def test_text_fields():
        """
        MS Excel CSV fields prefixed with '=' will be treated as equations to string.
        This makes it possible to e.g. to have all RPM version strings treated equally instead
        of making some of them treated as generic and some of them as integers.
        """
        _input = [dict(a=1, b=2)]
        expected = '\r\n'.join(['sep=,',
                                '"a",="b"',
                                '"1",="2"'])
        assert CsvConverter(_input).convert_to_ms_excel(text_fields=['b']) == expected

    @staticmethod
    def test_field_with_beginning_minus_is_prefixed():
        """
        MS Excel CSV fields beginning with '-' are treated as an equation even they would be
        essentially just strings. Make sure to escape the beginning signs with something in order
        not to get field braking equation.
        """
        _input = [dict(a=-1), dict(a="-2a")]
        expected = '\r\n'.join(['sep=,',
                                '"a"',
                                '"-1"',
                                r'"\-2a"'])
        assert CsvConverter(_input).convert_to_ms_excel() == expected

    @staticmethod
    def test_too_big_cell_is_truncated():
        """
        MS Excel has ~32k character limit per cell. BOM information can easily exceed this.
        """
        _input = [dict(a='1' * 32000), dict(a='2' * 32001)]
        expected = '\r\n'.join(['sep=,',
                                '"a"',
                                '"{}"'.format('1' * 32000),
                                '"{}...{}"'.format('2' * 16000, '2' * 16000)])
        assert CsvConverter(_input).convert_to_ms_excel() == expected
