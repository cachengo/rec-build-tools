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

import yaml

from tools.statics import PACKAGES_CONFIG_PATH


class PackageConfigReader(object):
    def __init__(self, config_file=PACKAGES_CONFIG_PATH):
        self.config_file = config_file
        self.config = None
        self._read_file()

    def _read_file(self):
        with open(self.config_file, 'r') as fp:
            self.config = yaml.load(fp)

    def get(self, package_operation_type):
        return self._get_packages_by_type(package_operation_type)

    def _get_packages_by_type(self, package_operation_type):
        if self.config is None:
            return []
        if package_operation_type == 'install':
            return self._get_installed_packages()
        elif package_operation_type == 'uninstall':
            return self._get_uninstalled_packages()
        raise Exception('Never here')

    def _get_uninstalled_packages(self):
        return sorted([p for p in self.config if not self._is_install_package(p)])

    def _get_installed_packages(self):
        return sorted([p for p in self.config if self._is_install_package(p)])

    def _is_install_package(self, package):
        if self.config[package] is None:
            return True
        if self.config[package].get('uninstall') is True:
            return False
        return True
