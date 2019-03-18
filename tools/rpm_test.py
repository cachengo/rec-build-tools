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

import os
import re

import pytest

from tools.rpm import RpmInfoParser
from tools.rpm_test_data import \
    bash_expected, conntrack_tools_expected, cpp_expected, usbredir_expected, perl_compress_expected
from tools.test_data_rpm import \
    bash_rpm_info, cpp_rpm_info, conntrack_tools_rpm_info, usbredir_rpm_info, perl_compress_rpm_info


@pytest.mark.parametrize('rpm_info, expected_output', [
    (bash_rpm_info, bash_expected),
    (conntrack_tools_rpm_info, conntrack_tools_expected),
    (cpp_rpm_info, cpp_expected),
    (usbredir_rpm_info, usbredir_expected),
    (perl_compress_rpm_info, perl_compress_expected)
])
def test_parse_package(rpm_info, expected_output):
    parsed = RpmInfoParser().parse_package(rpm_info)
    assert parsed == expected_output


def test_parse_multiple():
    parsed = RpmInfoParser().parse_multiple('\n'.join([bash_rpm_info, conntrack_tools_rpm_info]))
    assert parsed == [bash_expected, conntrack_tools_expected]


def test_parse_file():
    test_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                             'rpm_info_installed.sample')
    parsed = RpmInfoParser().parse_file(test_file)
    with open(test_file, 'r') as f:
        expected_rpms = re.findall(r'^Name\s+:.*$', f.read(), re.MULTILINE)
    assert len(parsed) == len(expected_rpms)
