# -*- coding: utf-8 -*-
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
from tools.rpm_test_data import cpp_expected

yum_installed_output = """Loaded plugins: fastestmirror, priorities
Loading mirror speeds from cached hostfile
Installed Packages
Name        : non-repo-pkg-1
Arch        : x86_64
Version     : 1
Release     : 1
Repo        : installed

Name        : non-repo-pkg-2
Arch        : noarch
Version     : 2
Release     : 2
Repo        : installed
Obsoletes   : (none)

Name        : base-image-pkg
Arch        : x86_64
Version     : 3
Release     : 3
Repo        : installed
From repo   : base

Name        : internal-pkg
Arch        : noarch
Version     : 4
Release     : 4
Repo        : installed
From repo   : localrepo

Name        : 3rdparty-pkg
Arch        : x86_64
Version     : 5
Release     : 5
Repo        : installed
From repo   : purkki-3rdparty
Obsoletes   : 2ndparty-pkg

"""

rpm_info_output = """Name        : non-repo-pkg-1
Version     : 1
Release     : 1
Architecture: x86_64
Source RPM  : non-repo-pkg-1-1-1.src.rpm
Name        : non-repo-pkg-2
Version     : 2
Release     : 2
Architecture: noarch
Source RPM  : non-repo-pkg-2-2-2.src.rpm
Name        : base-image-pkg
Version     : 3
Release     : 3
Architecture: x86_64
Source RPM  : base-image-pkg-3-3.src.rpm
Name        : internal-pkg
Version     : 4
Release     : 4
Architecture: noarch
Source RPM  : internal-pkg-4-4.src.rpm
Name        : 3rdparty-pkg
Version     : 5
Release     : 5
Architecture: x86_64
Source RPM  : 3rdparty-pkg-5-5.src.rpm
"""  # noqa, PEP-8 disabled because of example output has trailing spaces

yum_available_output_header = """Added tmprepo repo from http://url1/
Available Packages
"""

yum_available_output_base = """
Name        : base-image-pkg
Arch        : x86_64
Epoch       : 0
Version     : 3
Release     : 3
Size        : 195 k
Repo        : base
"""

yum_available_output_none2 = """
Name        : non-repo-pkg-1
Arch        : x86_64
Epoch       : 0
Version     : 1
Release     : 1
Size        : 195 k
Repo        : none2
"""

yum_available_output_none1 = """
Name        : non-repo-pkg-2
Arch        : noarch
Version     : 2
Release     : 2
Size        : 195 k
Repo        : none1
"""

yum_available_output_localrepo = """
Name        : internal-pkg
Arch        : x86_64
Epoch       : 0
Version     : 4
Release     : 4
Size        : 195 k
Repo        : localrepo
"""

yum_available_output_purkki_3rdparty = """
Name        : 3rdparty-pkg
Arch        : x86_64
Epoch       : 0
Version     : 5
Release     : 5
Size        : 195 k
Repo        : purkki-3rdparty
"""

yum_available_output = yum_available_output_header + yum_available_output_base + \
                       yum_available_output_none1 + yum_available_output_none2 + \
                       yum_available_output_localrepo + yum_available_output_purkki_3rdparty

internal_pkg_bom = [{'name': '@types/d3-axis',
                     'version': '1.0.10',
                     'foss': 'yes',
                     'source-url': 'http://some.url/1',
                     'crypto-capable': True},
                    {'name': '@types/d3-array@*',
                     'version': '1.2.1',
                     'foss': 'Yes',
                     'source-url': 'http://some.url/2'}]
boms_output = {'internal-pkg-4-4.noarch': {"bom": internal_pkg_bom}}

expected_output = [
    {
        'Name': 'non-repo-pkg-1',
        'Architecture': 'x86_64',
        'Version': '1',
        'Release': '1',
        'Repo': 'installed',
        'Repo data': {'baseurl': 'test-url-for-none2', 'name': 'none2'},
        'Obsoletes': 'N/A',
        'Source RPM': 'non-repo-pkg-1-1-1.src.rpm',
        'Crypto capable': False,
        'BOM': '',
    }, {
        'Name': 'non-repo-pkg-2',
        'Architecture': 'noarch',
        'Version': '2',
        'Release': '2',
        'Repo': 'installed',
        'Repo data': {'baseurl': 'test-url-for-none1', 'name': 'none1'},
        'Obsoletes': 'N/A',
        'Source RPM': 'non-repo-pkg-2-2-2.src.rpm',
        'Crypto capable': False,
        'BOM': '',
    }, {
        'Name': 'base-image-pkg',
        'Architecture': 'x86_64',
        'Version': '3',
        'Release': '3',
        'Repo': 'installed',
        'From repo': 'base',
        'Repo data': {'baseurl': 'test-url-for-base', 'name': 'base'},
        'Obsoletes': 'N/A',
        'Source RPM': 'base-image-pkg-3-3.src.rpm',
        'Crypto capable': False,
        'BOM': '',
    }, {
        'Name': 'internal-pkg',
        'Architecture': 'noarch',
        'Version': '4',
        'Release': '4',
        'Repo': 'installed',
        'From repo': 'localrepo',
        'Repo data': {'baseurl': 'test-url/artifact/results/repo',
                      'name': 'localrepo'},
        'Obsoletes': 'N/A',
        'Source RPM': 'internal-pkg-4-4.src.rpm',
        'Crypto capable': True,
        'BOM': internal_pkg_bom,
    }, {
        'Name': '3rdparty-pkg',
        'Architecture': 'x86_64',
        'Version': '5',
        'Release': '5',
        'Repo': 'installed',
        'From repo': 'purkki-3rdparty',
        'Repo data': {'baseurl': 'test-url-for-purkki-3rdparty', 'name': 'purkki-3rdparty',
                      'test-extra-option': 'test-value'},
        'Obsoletes': '2ndparty-pkg',
        'Source RPM': '3rdparty-pkg-5-5.src.rpm',
        'Crypto capable': False,
        'BOM': '',
    }]

basesystem_combined = {
    # From RPM info
    'Name': 'basesystem',
    'Version': '10.0',
    'Release': '7.el7.centos',
    'Architecture': 'noarch',
    'Install Date': 'Fri 01 Apr 2016 11:47:25 AM EEST',
    'Group': 'System Environment/Base',
    'Size': '0',
    'License': 'Public Domain',
    'Signature': 'RSA/SHA256, Fri 04 Jul 2014 03:46:57 AM EEST, Key ID 24c6a8a7f4a80eb5',
    'Source RPM': 'basesystem-10.0-7.el7.centos.src.rpm',
    'Build Date': 'Fri 27 Jun 2014 01:37:10 PM EEST',
    'Build Host': 'worker1.bsys.centos.org',
    'Relocations': '(not relocatable)',
    'Packager': 'CentOS BuildSystem <http://bugs.centos.org>',
    'Vendor': 'CentOS',
    'Summary': 'The skeleton package which defines a simple CentOS Linux system',
    'Description': '\n'.join(
        ['Basesystem defines the components of a basic CentOS Linux',
         'system (for example, the package installation order to use during',
         'bootstrapping). Basesystem should be in every installation of a system,',
         'and it should never be removed.']),
    # From yum info
    'Repo': 'installed',
}

centos_logos_combined = {
    'Name': 'centos-logos',
    'Version': '70.0.6',
    'Release': '3.el7.centos',
    'Architecture': 'noarch',
    'License': u'Copyright © 2014 The CentOS Project.  All rights reserved.',
}

cpp_combined = cpp_expected.copy()
cpp_combined.update({'Repo': 'installed',
                     'From repo': 'purkki-centos-base'})

dejavu_fonts_common_combined = {
    'Name': 'dejavu-fonts-common',
    'Version': '2.33',
    'Release': '6.el7',
    'Architecture': 'noarch',
    'Install Date': 'Wed Feb  7 13:49:27 2018',
    'Group': 'User Interface/X',
    'Size': '130455',
    'License': 'Bitstream Vera and Public Domain',
    'Signature': 'RSA/SHA256, Fri Jul  4 01:06:50 2014, Key ID 24c6a8a7f4a80eb5',
    'Source RPM': 'dejavu-fonts-2.33-6.el7.src.rpm',
    'Build Date': 'Mon Jun  9 21:34:30 2014',
    'Build Host': 'worker1.bsys.centos.org',
    'Relocations': '(not relocatable)',
    'Packager': 'CentOS BuildSystem <http://bugs.centos.org>',
    'Vendor': 'CentOS',
    'URL': 'http://dejavu-fonts.org/',
    'Summary': 'Common files for the Dejavu font set',
    'Description': '\n'.join(
        ['The DejaVu font set is based on the “Bitstream Vera” fonts, release 1.10. Its',
         'purpose is to provide a wider range of characters, while maintaining the',
         'original style, using an open collaborative development process.',
         '',
         'This package consists of files used by other DejaVu packages.']),
    'Repo': 'installed',
    'From repo': 'purkki-centos-base'
}

crypto_rpms_json = """
[
    {
        "name": "internal-pkg-4-4.noarch",
        "requires": [
            "libgssapi_krb5.so.2()(64bit)",
            "libk5crypto.so.3()(64bit)",
            "libkrb5.so.3()(64bit)",
            "libcrypto.so.10()(64bit)",
            "libcrypto.so.10(OPENSSL_1.0.1_EC)(64bit)",
            "libcrypto.so.10(OPENSSL_1.0.2)(64bit)",
            "libcrypto.so.10(libcrypto.so.10)(64bit)",
            "libssl.so.10()(64bit)",
            "libssl.so.10(libssl.so.10)(64bit)",
            "openssl-libs(x86-64)",
            "rtld(GNU_HASH)"
        ]
    }
]
"""
