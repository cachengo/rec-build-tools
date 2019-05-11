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
import os
import sys
import logging
import pytest
import mock

from tools.script.create_rpm_data import RpmDataBuilder
from tools.repository import BuildConfigParser
from tools.executor import Result
import tools.repository
from tools.script.create_rpm_data_test_data import \
    yum_installed_output, \
    rpm_info_output, \
    expected_output, \
    basesystem_combined, \
    cpp_combined, \
    centos_logos_combined, \
    dejavu_fonts_common_combined, yum_available_output, \
    crypto_rpms_json, boms_output

from tools.test_data_rpm import basesystem_rpm_info, cpp_rpm_info, centos_logos_rpm_info, \
    dejavu_fonts_common_rpm_info
from tools.test_data_yum import basesystem_yum_info, cpp_yum_info, centos_logos_yum_info, \
    dejavu_fonts_common_yum_info
from tools.yum import YumConfig


@mock.patch.object(YumConfig, 'write')
@mock.patch.object(tools.yum, 'run')
@mock.patch.object(BuildConfigParser, 'items')
def test_complete_parse(mock_config, mock_reporeader, _):
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    mock_config.side_effect = [
        [('base', 'test-url-for-base'),
         ('none1', 'test-url-for-none1'),
         ('none2', 'test-url-for-none2')],
        [('purkki-3rdparty', 'test-url-for-purkki-3rdparty#test-extra-option=test-value')],
        [('base', 'src-test-url-for-base'),
         ('none1', 'src-test-url-for-none1'),
         ('none2', 'src-test-url-for-none2')],
        [('purkki-3rdparty', 'src-test-url-for-purkki-3rdparty#test-extra-option2=test-value2')]
    ]
    mock_reporeader.side_effect = [Result(0, '', ''),  # yum clean all
                                   Result(0, '', ''),  # rm -rf /var/yum/cache
                                   Result(0, yum_available_output, '')]
    os.environ['BUILD_URL'] = 'test-url/'
    os.environ['WORK'] = '/foo/path'
    result = RpmDataBuilder('fake_build_config_path',
                            yum_installed_output,
                            rpm_info_output,
                            crypto_rpms_json,
                            boms_output).run()
    assert mock_reporeader.call_count == 3
    assert result == expected_output


@pytest.mark.parametrize('yum_info, rpm_info, expected_combined', [
    (basesystem_yum_info, basesystem_rpm_info, basesystem_combined),
    (cpp_yum_info, cpp_rpm_info, cpp_combined),
    (centos_logos_yum_info, centos_logos_rpm_info, centos_logos_combined),
    (dejavu_fonts_common_yum_info, dejavu_fonts_common_rpm_info, dejavu_fonts_common_combined),
])
def test_combine_rpm_data(yum_info, rpm_info, expected_combined):
    result = RpmDataBuilder('fake_build_config_path',
                            yum_info,
                            rpm_info,
                            '[]',
                            {}).read_installed_rpms()
    assert result[0] == expected_combined
