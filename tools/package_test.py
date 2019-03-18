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

import mock

from tools.package import PackageConfigReader


def test_packages():
    with mock.patch('tools.package.open', mock.mock_open(read_data=FAKE_PACKAGES_YAML)) as _:
        config = PackageConfigReader('test-config')
    assert config.get('install') == ['install-pkg-1',
                                     'install-pkg-2']
    assert config.get('uninstall') == ['remove-pkg-1',
                                       'remove-pkg-2']


def test_empty():
    with mock.patch('tools.package.open', mock.mock_open(read_data="")) as _:
        config = PackageConfigReader('test-config')
    assert config.get('install') == []


FAKE_PACKAGES_YAML = """
remove-pkg-1:
    uninstall: True
remove-pkg-2:
    uninstall: True

install-pkg-1:
    uninstall: False
install-pkg-2:
"""
