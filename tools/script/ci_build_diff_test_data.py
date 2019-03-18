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

# pylint: disable=line-too-long,invalid-name
import re

from copy import deepcopy


def _copy(d, pattern, repl):
    x = deepcopy(d)
    for k, v in x.items():
        if isinstance(v, str):
            x[k] = re.sub(pattern, repl, v)
    return x


caas_grafana1 = {
    "Architecture": "noarch",
    "Build Date": "Wed May 30 11:39:05 2018",
    "Build Host": "crf-dev",
    "Crypto capable": False,
    "Description": "This is grafana, this is SPARTAAAAA!",
    "FOSS": "No",
    "From repo": "caas-artifactory",
    "Group": "Unspecified",
    "Install Date": "Sun Nov 18 22:15:41 2018",
    "Is sane": True,
    "License": "Commercial",
    "Name": "caas.grafana",
    "Obsoletes": "",
    "Release": "1.el7.centos",
    "Relocations": "(not relocatable)",
    "Repo": "installed",
    "Repo data": {
        "baseurl": "http://files/20181023",
        "name": "caas-artifactory"
    },
    "Signature": "(none)",
    "Size": "109683450",
    "Source RPM": "caas.grafana-4.4.1.9-1.el7.centos.src.rpm",
    "Source repo data": {
        "baseurl": "http://files/20181023",
        "name": "caas-artifactory"
    },
    "Source to be delivered": "No",
    "Summary": "caasgrafana",
    "Vendor": "Something",
    "Version": "4.4.1.9"
}

caas_grafana1_sub = {
    "Name": "grafana",
    "Version": "4.4.1.9",
    "Source RPM": "caas.grafana-4.4.1.9-1.el7.centos.src.rpm",
    "Source URL": "https://some/grafana/url",
    "FOSS": "yes"
}

caas_grafana1_sub_new_field = deepcopy(caas_grafana1_sub)
caas_grafana1_sub_new_field['ABC'] = True

caas_grafana2 = _copy(caas_grafana1, 'caas.grafana', 'caas.grafana2')
caas_grafana2_sub = _copy(caas_grafana1_sub, 'caas.grafana', 'caas.grafana2')

caas_grafana3 = _copy(caas_grafana1, 'caas.grafana', 'caas.grafana3')
caas_grafana3_sub = _copy(caas_grafana1_sub, 'caas.grafana', 'caas.grafana3')

caas_grafana1_v2 = _copy(caas_grafana1, '4.4.1.9', '4.4.1.10')
caas_grafana1_v2sub = _copy(caas_grafana1_sub, '4.4.1.9', '4.4.1.10')

caas_grafana1_r2 = _copy(caas_grafana1, '1.el7.centos', '2.el7.centos')
caas_grafana1_r2sub = _copy(caas_grafana1_sub, '1.el7.centos', '2.el7.centos')

caas_abc1 = {
    "License": "Commercial",
    "Name": "caas-abc",
    "Version": "v1",
    "Release": "r1",
    "Source RPM": "caas-abc-v1-r1.src.rpm",
}

caas_abc1_sub = {
    "Name": "abc",
    "Version": "v1",
    "Source RPM": "caas-abc-v1-r1.src.rpm",
}
caas_abc1_r2 = _copy(caas_abc1, 'r1', 'r2')
caas_abc1_sub_r2 = _copy(caas_abc1_sub, 'r1', 'r2')

abc1 = {
    "License": "GPL",
    "Name": "abc",
    "Version": "v1",
    "Release": "r1",
    "Source RPM": "abc-v1-r1.src.rpm",
}
abc1_v2 = _copy(abc1, 'v1', 'v2')
abc2 = _copy(abc1, 'abc', 'abc2')
abc3 = _copy(abc1, 'abc', 'abc3')

component_added = {
    'Architecture': 'noarch',
    'Build Date': 'Sun Nov 11 12:54:39 2018',
    'Build Host': 'build-7.novalocal',
    'Description': 'This RPM contains configuration management openstack configuration override '
                   'plugin',
    'FOSS': 'No',
    'From repo': 'localrepo',
    'Group': 'Unspecified',
    'Install Date': 'Tue Nov 13 19:14:29 2018',
    'Is sane': True,
    'License': 'Commercial',
    'Name': 'openstack-config-overrides-validator',
    'Obsoletes': '',
    'Packager': 'Something',
    'Release': '1.el7.centos',
    'Relocations': '(not relocatable)',
    'Repo': 'installed',
    'Repo data': {
        'baseurl': 'https://jenkins/ci-build/2490/artifact/results/repo',
        'name': 'localrepo'},
    'Signature': '(none)',
    'Size': '3097',
    'Source RPM': 'openstack-config-overrides-validator-c2.gd1b7aec-1.el7.centos.src.rpm',
    'Source repo data': {
        'baseurl': 'https://jenkins/ci-build/2490/artifact/results/src_repo',
        'name': 'localrepo'},
    'Source to be delivered': 'No',
    'Summary': 'Openstack configuration override CM validator plugin.',
    'Vendor': 'Something',
    'Version': 'c2.gd1b7aec'
}

component_removed = {
    'Architecture': 'x86_64',
    'Build Date': 'Thu Aug 16 14:46:11 2018',
    'Build Host': 'x86-01.bsys.centos.org',
    'Description': 'The fence-agents-ibmblade package contains a fence agent for IBM BladeCenter '
                   'devices that are accessed via the SNMP protocol.',
    'FOSS': 'Undefined',
    'From repo': 'purkki-centos-updates',
    'Group': 'System Environment/Base',
    'Install Date': 'Wed Nov  7 21:20:01 2018',
    'Is sane': False,
    'License': 'GPLv2+ and LGPLv2+',
    'Name': 'fence-agents-ibmblade',
    'Obsoletes': 'fence-agents,',
    'Packager': 'CentOS BuildSystem <http://bugs.centos.org>',
    'Release': '86.el7_5.3',
    'Relocations': '(not relocatable)',
    'Repo': 'installed',
    'Repo data': {
        'baseurl': 'http://purkki/mirror/centos/snapshot/20181024/7/updates/x86_64/',
        'exclude': 'libgudev1 httpd httpd-devel systemd-libs.i686 resource-agents '
                   'dhcp-libs dhclient dhcp-common php-fpm php-common php-cli php',
        'name': 'purkki-centos-updates'},
    'Signature': 'RSA/SHA256, Mon Aug 20 14:15:17 2018, Key ID 24c6a8a7f4a80eb5',
    'Size': '3898',
    'Source RPM': 'fence-agents-4.0.11-86.el7_5.3.src.rpm',
    'Source repo data': {
        'baseurl': 'http://purkki/mirror/centos/snapshot/20181024/7/updates/Source/',
        'name': 'purkki-centos-updates'},
    'Source to be delivered': 'Undefined',
    'Summary': 'Fence agent for IBM BladeCenter',
    'URL': 'https://github.com/ClusterLabs/fence-agents',
    'Vendor': 'CentOS',
    'Version': '4.0.11'
}
component_changed_old = {
    'Architecture': 'noarch',
    'Build Date': 'Fri Oct 19 00:22:00 2018',
    'Build Host': 'f32725a719ce4c82a53b44644dfd2718',
    'Description': 'This RPM contains source code for the Authentication, Authorization and '
                   'Accounting cli',
    'FOSS': 'No',
    'From repo': 'localrepo',
    'Group': 'Unspecified',
    'Install Date': 'Wed Nov  7 21:22:14 2018',
    'Is sane': True,
    'License': 'Commercial',
    'Name': 'aaacli',
    'Obsoletes': '',
    'Packager': 'Something',
    'Release': '2.el7.centos',
    'Relocations': '(not relocatable)',
    'Repo': 'installed',
    'Repo data': {
        'baseurl': 'https://jenkins/ci-build/2432/artifact/results/repo',
        'name': 'localrepo'},
    'Signature': '(none)',
    'Size': '43968',
    'Source RPM': 'aaacli-c12.gc62d348-2.el7.centos.src.rpm',
    'Source repo data': {
        'baseurl': 'https://jenkins/ci-build/2432/artifact/results/src_repo',
        'name': 'localrepo'},
    'Source to be delivered': 'No',
    'Summary': 'Authentication, Authorization and Accounting Command Line Interface',
    'Vendor': 'Something',
    'Version': 'c12.gc62d348'
}

component_changed_new = {
    'Architecture': 'noarch',
    'Build Date': 'Thu Nov  8 05:05:07 2018',
    'Build Host': 'build-3.novalocal',
    'Description': 'This RPM contains source code for the Authentication, '
                   'Authorization and Accounting cli',
    'FOSS': 'No',
    'From repo': 'localrepo',
    'Group': 'Unspecified',
    'Install Date': 'Tue Nov 13 19:09:30 2018',
    'Is sane': True,
    'License': 'Commercial',
    'Name': 'aaacli',
    'Obsoletes': '',
    'Packager': 'Something',
    'Release': '1.el7.centos',
    'Relocations': '(not relocatable)',
    'Repo': 'installed',
    'Repo data': {
        'baseurl': 'https://jenkins/ci-build/2490/artifact/results/repo',
        'name': 'localrepo'},
    'Signature': '(none)',
    'Size': '44034',
    'Source RPM': 'aaacli-c13.gcb6b490-1.el7.centos.src.rpm',
    'Source repo data': {
        'baseurl': 'https://jenkins/ci-build/2490/artifact/results/src_repo',
        'name': 'localrepo'},
    'Source to be delivered': 'No',
    'Summary': 'Authentication, Authorization and Accounting Command Line Interface',
    'Vendor': 'Something',
    'Version': 'c13.gcb6b490'
}

grafana_v1 = {
    'Architecture': 'x86_64',
    'Build Date': 'Mon Sep 17 14:30:25 2018',
    'Build Host': 'd8fb00edf57f4254bb45073a941929ff',
    'Description': 'Grafana is an open source, feature rich metrics dashboard and graph '
                   'editor for\nGraphite, InfluxDB & OpenTSDB.',
    'FOSS': 'Modified',
    'From repo': 'localrepo',
    'Group': 'Unspecified',
    'Install Date': 'Fri Nov 16 02:23:02 2018',
    'Is sane': True,
    'License': 'Commercial and  ASL 2.0 and others',
    'Name': 'grafana',
    'Obsoletes': '',
    'Packager': 'Something',
    'Release': '1.el7.centos.1',
    'Relocations': '(not relocatable)',
    'Repo': 'installed',
    'Repo data': {
        'baseurl': 'https://jenkins/ci-build/2506/artifact/results/repo',
        'name': 'localrepo'},
    'Signature': '(none)',
    'Size': '93957067',
    'Source RPM': 'grafana-5.2.3-1.el7.centos.1.src.rpm',
    'Source repo data': {
        'baseurl': 'https://jenkins/ci-build/2506/artifact/results/src_repo',
        'name': 'localrepo'},
    'Source to be delivered': 'Upstream',
    'Summary': 'Grafana is an open source, feature rich metrics dashboard and graph editor',
    'URL': 'https://github.com/grafana/grafana',
    'Vendor': 'Something and Grafana modified',
    'Version': '5.2.3'
}

grafana_v2 = _copy(grafana_v1, '1.el7.centos.1', '1.el7.centos.2')
