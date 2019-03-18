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

# pylint: disable=invalid-name,line-too-long

yum_info_installed_header = """Loaded plugins: fastestmirror, priorities
Loading mirror speeds from cached hostfile
Installed Packages
"""

yum_info_available_header = """Added tmprepo repo from http://purkki/mirror/centos/snapshot/20170705-2/7/os/x86_64/
Available Packages
"""  # noqa

yum_info_available_header2 = """Available Packages
"""

bash_expected = {
    'Name': 'bash',
    'Arch': 'x86_64',
    'Version': '4.2.46',
    'Release': '21.el7_3',
    'Size': '3.5 M',
    'Repo': 'installed',
    'From repo': 'updates',
    'Summary': 'The GNU Bourne Again shell',
    'URL': 'http://www.gnu.org/software/bash',
    'License': 'GPLv3+',
    'Description': '\n'.join(
        ['The GNU Bourne Again shell (Bash) is a shell or command language',
         'interpreter that is compatible with the Bourne shell (sh). Bash',
         'incorporates useful features from the Korn shell (ksh) and the C',
         'shell (csh). Most sh scripts can be run by bash without',
         'modification.'])
}

conntrack_tools_expected = {
    'Name': 'conntrack-tools',
    'Arch': 'x86_64',
    'Version': '1.4.4',
    'Release': '3.el7_3',
    'Size': '550 k',
    'Repo': 'installed',
    'From repo': 'centos-updates',
    'Summary': ' '.join(
        ['Manipulate netfilter connection tracking table and run High',
         'Availability']),
    'URL': 'http://netfilter.org',
    'License': 'GPLv2',
    'Description': '\n'.join(
        ['With conntrack-tools you can setup a High Availability cluster and',
         'synchronize conntrack state between multiple firewalls.',
         '',
         'The conntrack-tools package contains two programs:',
         '- conntrack: the command line interface to interact with the',
         '  connection tracking system.',
         '- conntrackd: the connection tracking userspace daemon that can be',
         '  used to deploy highly available GNU/Linux firewalls and collect',
         '              statistics of the firewall use.',
         '',
         'conntrack is used to search, list, inspect and maintain the',
         'netfilter connection tracking subsystem of the Linux kernel.',
         'Using conntrack, you can dump a list of all (or a filtered',
         'selection  of) currently tracked connections, delete connections',
         'from the state table, and even add new ones.',
         'In addition, you can also monitor connection tracking events, e.g.',
         'show an event message (one line) per newly established connection.'])
}

pacemaker_expected = {
    'Name': 'pacemaker',
    'Arch': 'x86_64',
    'Version': '1.1.15',
    'Release': '11.el7_3.5',
    'Size': '1.1 M',
    'Repo': 'installed',
    'From repo': 'purkki-centos-updates',
    'Summary': 'Scalable High-Availability cluster resource manager',
    'URL': 'http://www.clusterlabs.org',
    'License': 'GPLv2+ and LGPLv2+',
    'Description': '\n'.join(
        ['Pacemaker is an advanced, scalable High-Availability cluster',
         'resource manager for Corosync, CMAN and/or Linux-HA.',
         '',
         'It supports more than 16 node clusters with significant',
         'capabilities for managing resources and dependencies.',
         '',
         'It will run scripts at initialization, when machines go up or',
         'down, when related resources fail and can be configured to',
         'periodically check resource health.',
         '',
         'Available rpmbuild rebuild options:',
         '  --with(out) : cman stonithd doc coverage profiling pre_release',
         'hardening'])
}
