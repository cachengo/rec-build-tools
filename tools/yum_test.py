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

# pylint: disable=wildcard-import
import os
import pytest

from tools.test_data_yum import bash_yum_info, \
    conntrack_tools_yum_info, \
    pacemaker_yum_info
from tools.yum import YumInfoParser
from tools.yum_test_data import bash_expected, pacemaker_expected, \
    yum_info_installed_header, \
    yum_info_available_header, \
    yum_info_available_header2
from tools.yum_test_data import conntrack_tools_expected


@pytest.mark.parametrize('yum_info, expected_output', [
    (bash_yum_info, bash_expected),
    (conntrack_tools_yum_info, conntrack_tools_expected),
    (pacemaker_yum_info, pacemaker_expected)
])
def test_parse_package(yum_info, expected_output):
    parsed = YumInfoParser().parse_package(yum_info)
    expected = expected_output
    assert parsed == expected


def test_parse_installed():
    fake_out = '\n'.join([yum_info_installed_header,
                          bash_yum_info,
                          conntrack_tools_yum_info])
    parsed = YumInfoParser().parse_installed(fake_out)
    expected = [bash_expected, conntrack_tools_expected]
    assert parsed == expected


@pytest.mark.parametrize('available_header', [
    yum_info_available_header,
    yum_info_available_header2
])
def test_parse_available(available_header):
    fake_out = '\n'.join([available_header,
                          bash_yum_info,
                          conntrack_tools_yum_info])
    parsed = YumInfoParser().parse_available(fake_out)
    expected = [bash_expected, conntrack_tools_expected]
    assert parsed == expected


def test_parse_file():
    test_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                             'yum_info_installed.sample')
    parsed = YumInfoParser().parse_file(test_file)
    assert len(parsed) == 14
