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

import re


class RpmData(dict):

    @property
    def name(self):
        return self['Name']

    @property
    def epoch(self):
        return self.get('Epoch', '0')

    @property
    def version(self):
        return self['Version']

    @property
    def release(self):
        return self['Release']

    @property
    def arch(self):
        return self['Architecture']

    @property
    def vendor(self):
        return self.get('Vendor', '')

    @property
    def license(self):
        return self.get('License', '')

    def __str__(self):
        return '{}-{}-{}.{}'.format(self.name,
                                    self.version,
                                    self.release,
                                    self.arch)

    def is_same_package_as(self, other):
        for attr in ['name', 'epoch', 'version', 'release', 'arch']:
            if getattr(self, attr) != getattr(other, attr):
                return False
        return True


class RpmInfoParser(object):
    """
    Parse 'rpm -qi' output
    """

    def parse_file(self, rpm_info_installed_file_path):
        with open(rpm_info_installed_file_path, 'r') as f:
            return self.parse_multiple(f.read())

    def parse_multiple(self, rpm_info_output_multiple):
        packages = []
        package_index = -1
        for line in rpm_info_output_multiple.splitlines():
            if re.match(r'^Name\s+:.*', line):
                packages.append(line)
                package_index += 1
            else:
                packages[package_index] += '\n' + line
        return [self.parse_package(pkg) for pkg in packages]

    @staticmethod
    def parse_package(rpm_info_output):
        result = RpmData()
        current_key = None
        colon_location = rpm_info_output.splitlines()[0].find(':')
        matcher = re.compile(r'^([A-Z][A-Za-z0-9 ]{{{}}}):( ?| .+)$'.format(colon_location - 1))
        for line in rpm_info_output.splitlines():
            match = matcher.match(line)
            if match:
                parsed_key = match.group(1).rstrip()
                parsed_value = match.group(2).strip()
                result[parsed_key] = parsed_value
                current_key = parsed_key
            else:
                if not result[current_key]:
                    result[current_key] = line
                else:
                    result[current_key] = result[current_key] + '\n' + line
        return result
