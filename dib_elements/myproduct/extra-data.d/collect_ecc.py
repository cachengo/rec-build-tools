#!/usr/bin/python
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

import subprocess
import json
import sys

# following libs are found from openssl, libgcrypto, openssh with rpm -qR
# in the future, the libs need to be updated with exact version number

input_capabilities = []
output_rpms = []
input_packages = [
                  'openssl',
                  'openssh',
                  'p11-kit',
                  'openssl-libs',
                  'libgcrypt',
                  'libgcrypt.so',
                  'python2-cryptography',
                  'sshpass',
                  'm2crypto',
                  'erlang-crypto',
                  'openssh-clients',
                  'python2-passlib',
                  'python-paramiko',
                  'python-keyring',
                  'python2-asn1crypto',
                  'python2-cryptography',
                  'python2-pyasn1',
                  'xstatic-jsencrypt-common',
                  'krb5-libs'
                 ]
crypto_capabilities = [
                       'rtld(',
                       'libcrypt.so'
                      ]


def output_rpm_command(lib, command):
    command.append(lib)
    try:
        output = subprocess.check_output(command)
    except:
        output = ""
    return output


def build_capability_list_dynamically():
    map_dict = {}
    command = ['rpm',
               '-qa',
               '--queryformat',
               '[%{=NAME}-%{VERSION}-%{RELEASE}.%{ARCH} %{PROVIDES}\n]']
    output = subprocess.check_output(command)
    for item in output.splitlines():
        items = item.split(' ')
        if items:
            if items[0] in map_dict:
                capa_list = map_dict[items[0]]
                capa_list.append(items[1])
                map_dict[items[0]] = capa_list
            else:
                map_dict[items[0]] = [items[1]]
    for rpms, caps in map_dict.items():
        for cap in caps:
            for item in crypto_capabilities:
                if cap.startswith(item):
                    if cap not in input_capabilities:
                        input_capabilities.append(cap)
                        command = ['rpm', '-q', '--whatprovides']
                        output = output_rpm_command(cap, command)
                        name = output.strip('\n')
                        result = filter(lambda rpm: rpm['name'] == name, output_rpms)
                        if not result:
                            output_rpms.append({'name': name, 'provides': [cap]})
                        else:
                            sources_list = result[0]['provides']
                            if cap not in sources_list:
                                sources_list.append(cap)


def capability_dependencies_with_whatrequires():
    for capability in input_capabilities:
        command = ['rpm', '-q', '--whatrequires']
        output = output_rpm_command(capability, command)
        if output:
            for item in output.splitlines():
                result = filter(lambda rpm: rpm['name'] == item, output_rpms)
                if not result:
                    output_rpms.append({'name': item, 'requires': [capability]})
                else:
                    sources_list = result[0]['requires']
                    if capability not in sources_list:
                        sources_list.append(capability)


def package_dependencies_with_provides():
    for package in input_packages:
        command = ['rpm', '-q']
        name = output_rpm_command(package, command)
        name = name.strip('\n')
        output_rpms.append({'name': name, 'requires': []})
        command = ['rpm', '-ql', '--provides']
        output = output_rpm_command(package, command)
        for item in output.splitlines():
            input_capabilities.append(item)


if __name__ == '__main__':
    build_capability_list_dynamically()
    package_dependencies_with_provides()
    capability_dependencies_with_whatrequires()
    rpms_json = json.dumps(output_rpms, sort_keys=True, indent=4)
    with open(sys.argv[1], "w") as f:
        f.write(rpms_json)
