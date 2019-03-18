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


basesystem_yum_info = """Loaded plugins: fastestmirror, priorities
Loading mirror speeds from cached hostfile
Installed Packages
Name        : basesystem
Arch        : noarch
Version     : 10.0
Release     : 7.el7.centos
Size        : 0.0  
Repo        : installed
Summary     : The skeleton package which defines a simple CentOS Linux system
License     : Public Domain
Description : Basesystem defines the components of a basic CentOS Linux
            : system (for example, the package installation order to use during
            : bootstrapping). Basesystem should be in every installation of a
            : system, and it should never be removed.

"""  # noqa, PEP-8 disabled because of example output has trailing spaces

bash_yum_info = """Name        : bash
Arch        : x86_64
Version     : 4.2.46
Release     : 21.el7_3
Size        : 3.5 M
Repo        : installed
From repo   : updates
Summary     : The GNU Bourne Again shell
URL         : http://www.gnu.org/software/bash
License     : GPLv3+
Description : The GNU Bourne Again shell (Bash) is a shell or command language
            : interpreter that is compatible with the Bourne shell (sh). Bash
            : incorporates useful features from the Korn shell (ksh) and the C
            : shell (csh). Most sh scripts can be run by bash without
            : modification.
"""

centos_logos_yum_info = """
Installed Packages
Name        : centos-logos
Arch        : noarch
Version     : 70.0.6
Release     : 3.el7.centos
License     : Copyright ? 2014 The CentOS Project.  All rights reserved.

"""

conntrack_tools_yum_info = """Name        : conntrack-tools
Arch        : x86_64
Version     : 1.4.4
Release     : 3.el7_3
Size        : 550 k
Repo        : installed
From repo   : centos-updates
Summary     : Manipulate netfilter connection tracking table and run High
            : Availability
URL         : http://netfilter.org
License     : GPLv2
Description : With conntrack-tools you can setup a High Availability cluster and
            : synchronize conntrack state between multiple firewalls.
            : 
            : The conntrack-tools package contains two programs:
            : - conntrack: the command line interface to interact with the
            :   connection tracking system.
            : - conntrackd: the connection tracking userspace daemon that can be
            :   used to deploy highly available GNU/Linux firewalls and collect
            :               statistics of the firewall use.
            : 
            : conntrack is used to search, list, inspect and maintain the
            : netfilter connection tracking subsystem of the Linux kernel.
            : Using conntrack, you can dump a list of all (or a filtered
            : selection  of) currently tracked connections, delete connections
            : from the state table, and even add new ones.
            : In addition, you can also monitor connection tracking events, e.g.
            : show an event message (one line) per newly established connection.
"""  # noqa, PEP-8 disabled because of example output has trailing spaces

cpp_yum_info = """
Installed Packages
Name        : cpp
Arch        : x86_64
Version     : 4.8.5
Release     : 11.el7
Size        : 15 M
Repo        : installed
From repo   : purkki-centos-base
Summary     : The C Preprocessor
URL         : http://gcc.gnu.org
License     : GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions and
            : LGPLv2+ and BSD
Description : Cpp is the GNU C-Compatible Compiler Preprocessor.
            : Cpp is a macro processor which is used automatically
            : by the C compiler to transform your program before actual
            : compilation. It is called a macro processor because it allows
            : you to define macros, abbreviations for longer
            : constructs.
            : 
            : The C preprocessor provides four separate functionalities: the
            : inclusion of header files (files of declarations that can be
            : substituted into your program); macro expansion (you can define
            : macros, and the C preprocessor will replace the macros with their
            : definitions throughout the program); conditional compilation
            : (using special preprocessing directives, you can include or
            : exclude parts of the program according to various conditions); and
            : line control (if you use a program to combine or rearrange source
            : files into an intermediate file which is then compiled, you can
            : use line control to inform the compiler about where each source
            : line originated).
            : 
            : You should install this package if you are a C programmer and you
            : use macros.

"""  # noqa, PEP-8 disabled because of example output has trailing spaces

dejavu_fonts_common_yum_info = """
Installed Packages
Name        : dejavu-fonts-common
Arch        : noarch
Version     : 2.33
Release     : 6.el7
Size        : 127 k
Repo        : installed
From repo   : purkki-centos-base
Summary     : Common files for the Dejavu font set
URL         : http://dejavu-fonts.org/
License     : Bitstream Vera and Public Domain
Description : 
            : The DejaVu font set is based on the ?Bitstream Vera? fonts,
            : release 1.10. Its purpose is to provide a wider range of
            : characters, while maintaining the original style, using an open
            : collaborative development process.
            : 
            : This package consists of files used by other DejaVu packages.

"""  # noqa, PEP-8 disabled because of example output has trailing spaces

pacemaker_yum_info = """
Name        : pacemaker
Arch        : x86_64
Version     : 1.1.15
Release     : 11.el7_3.5
Size        : 1.1 M
Repo        : installed
From repo   : purkki-centos-updates
Summary     : Scalable High-Availability cluster resource manager
URL         : http://www.clusterlabs.org
License     : GPLv2+ and LGPLv2+
Description : Pacemaker is an advanced, scalable High-Availability cluster
            : resource manager for Corosync, CMAN and/or Linux-HA.
            : 
            : It supports more than 16 node clusters with significant
            : capabilities for managing resources and dependencies.
            : 
            : It will run scripts at initialization, when machines go up or
            : down, when related resources fail and can be configured to
            : periodically check resource health.
            : 
            : Available rpmbuild rebuild options:
            :   --with(out) : cman stonithd doc coverage profiling pre_release
            : hardening
"""  # noqa, PEP-8 disabled because of example output has trailing spaces
