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

# pylint: disable=invalid-name,line-too-long

bash_rpm_info = """Name        : bash
Version     : 4.2.46
Release     : 21.el7_3
Architecture: x86_64
Install Date: Thu 11 Jan 2018 12:32:51 PM EET
Group       : System Environment/Shells
Size        : 3663714
License     : GPLv3+
Signature   : RSA/SHA256, Wed 07 Dec 2016 02:11:28 AM EET, Key ID 24c6a8a7f4a80eb5
Source RPM  : bash-4.2.46-21.el7_3.src.rpm
Build Date  : Wed 07 Dec 2016 01:21:54 AM EET
Build Host  : c1bm.rdu2.centos.org
Relocations : (not relocatable)
Packager    : CentOS BuildSystem <http://bugs.centos.org>
Vendor      : CentOS
URL         : http://www.gnu.org/software/bash
Summary     : The GNU Bourne Again shell
Description :
The GNU Bourne Again shell (Bash) is a shell or command language
interpreter that is compatible with the Bourne shell (sh). Bash
incorporates useful features from the Korn shell (ksh) and the C shell
(csh). Most sh scripts can be run by bash without modification.
"""

basesystem_rpm_info = """Name        : basesystem
Version     : 10.0
Release     : 7.el7.centos
Architecture: noarch
Install Date: Fri 01 Apr 2016 11:47:25 AM EEST
Group       : System Environment/Base
Size        : 0
License     : Public Domain
Signature   : RSA/SHA256, Fri 04 Jul 2014 03:46:57 AM EEST, Key ID 24c6a8a7f4a80eb5
Source RPM  : basesystem-10.0-7.el7.centos.src.rpm
Build Date  : Fri 27 Jun 2014 01:37:10 PM EEST
Build Host  : worker1.bsys.centos.org
Relocations : (not relocatable)
Packager    : CentOS BuildSystem <http://bugs.centos.org>
Vendor      : CentOS
Summary     : The skeleton package which defines a simple CentOS Linux system
Description :
Basesystem defines the components of a basic CentOS Linux
system (for example, the package installation order to use during
bootstrapping). Basesystem should be in every installation of a system,
and it should never be removed.
"""

centos_logos_rpm_info = u"""Name        : centos-logos
Version     : 70.0.6
Release     : 3.el7.centos
Architecture: noarch
License     : Copyright © 2014 The CentOS Project.  All rights reserved.

"""

conntrack_tools_rpm_info = """Name        : conntrack-tools
Version     : 1.4.4
Release     : 3.el7_3
Architecture: x86_64
Install Date: Thu 11 Jan 2018 12:39:20 PM EET
Group       : System Environment/Base
Size        : 562826
License     : GPLv2
Signature   : RSA/SHA256, Thu 29 Jun 2017 03:36:05 PM EEST, Key ID 24c6a8a7f4a80eb5
Source RPM  : conntrack-tools-1.4.4-3.el7_3.src.rpm
Build Date  : Thu 29 Jun 2017 03:18:42 AM EEST
Build Host  : c1bm.rdu2.centos.org
Relocations : (not relocatable)
Packager    : CentOS BuildSystem <http://bugs.centos.org>
Vendor      : CentOS
URL         : http://netfilter.org
Summary     : Manipulate netfilter connection tracking table and run High Availability
Description :
With conntrack-tools you can setup a High Availability cluster and
synchronize conntrack state between multiple firewalls.

The conntrack-tools package contains two programs:
- conntrack: the command line interface to interact with the connection
             tracking system.
- conntrackd: the connection tracking userspace daemon that can be used to
              deploy highly available GNU/Linux firewalls and collect
              statistics of the firewall use.

conntrack is used to search, list, inspect and maintain the netfilter
connection tracking subsystem of the Linux kernel.
Using conntrack, you can dump a list of all (or a filtered selection  of)
currently tracked connections, delete connections from the state table,
and even add new ones.
In addition, you can also monitor connection tracking events, e.g.
show an event message (one line) per newly established connection.
"""

cpp_rpm_info = """Name        : cpp
Version     : 4.8.5
Release     : 11.el7
Architecture: x86_64
Install Date: Thu 11 Jan 2018 12:37:55 PM EET
Group       : Development/Languages
Size        : 15632501
License     : GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions and LGPLv2+ and BSD
Signature   : RSA/SHA256, Sun 20 Nov 2016 07:27:00 PM EET, Key ID 24c6a8a7f4a80eb5
Source RPM  : gcc-4.8.5-11.el7.src.rpm
Build Date  : Fri 04 Nov 2016 06:01:22 PM EET
Build Host  : worker1.bsys.centos.org
Relocations : (not relocatable)
Packager    : CentOS BuildSystem <http://bugs.centos.org>
Vendor      : CentOS
URL         : http://gcc.gnu.org
Summary     : The C Preprocessor
Description :
Cpp is the GNU C-Compatible Compiler Preprocessor.
Cpp is a macro processor which is used automatically
by the C compiler to transform your program before actual
compilation. It is called a macro processor because it allows
you to define macros, abbreviations for longer
constructs.

The C preprocessor provides four separate functionalities: the
inclusion of header files (files of declarations that can be
substituted into your program); macro expansion (you can define macros,
and the C preprocessor will replace the macros with their definitions
throughout the program); conditional compilation (using special
preprocessing directives, you can include or exclude parts of the
program according to various conditions); and line control (if you use
a program to combine or rearrange source files into an intermediate
file which is then compiled, you can use line control to inform the
compiler about where each source line originated).

You should install this package if you are a C programmer and you use
macros.
"""  # noqa, PEP-8 disabled because of example output has trailing spaces

dejavu_fonts_common_rpm_info = """Name        : dejavu-fonts-common
Version     : 2.33
Release     : 6.el7
Architecture: noarch
Install Date: Wed Feb  7 13:49:27 2018
Group       : User Interface/X
Size        : 130455
License     : Bitstream Vera and Public Domain
Signature   : RSA/SHA256, Fri Jul  4 01:06:50 2014, Key ID 24c6a8a7f4a80eb5
Source RPM  : dejavu-fonts-2.33-6.el7.src.rpm
Build Date  : Mon Jun  9 21:34:30 2014
Build Host  : worker1.bsys.centos.org
Relocations : (not relocatable)
Packager    : CentOS BuildSystem <http://bugs.centos.org>
Vendor      : CentOS
URL         : http://dejavu-fonts.org/
Summary     : Common files for the Dejavu font set
Description :

The DejaVu font set is based on the “Bitstream Vera” fonts, release 1.10. Its
purpose is to provide a wider range of characters, while maintaining the
original style, using an open collaborative development process.

This package consists of files used by other DejaVu packages.
"""

usbredir_rpm_info = """Name        : usbredir
Version     : 0.7.1
Release     : 1.el7
Architecture: x86_64
Install Date: Wed Feb  7 13:49:24 2018
Group       : System Environment/Libraries
Size        : 108319
License     : LGPLv2+
Signature   : RSA/SHA256, Sun Nov 20 20:56:49 2016, Key ID 24c6a8a7f4a80eb5
Source RPM  : usbredir-0.7.1-1.el7.src.rpm
Build Date  : Sat Nov  5 18:33:15 2016
Build Host  : worker1.bsys.centos.org
Relocations : (not relocatable)
Packager    : CentOS BuildSystem <http://bugs.centos.org>
Vendor      : CentOS
URL         : http://spice-space.org/page/UsbRedir
Summary     : USB network redirection protocol libraries
Description :
The usbredir libraries allow USB devices to be used on remote and/or virtual
hosts over TCP.  The following libraries are provided:

usbredirparser:
A library containing the parser for the usbredir protocol

usbredirhost:
A library implementing the USB host side of a usbredir connection.
All that an application wishing to implement a USB host needs to do is:
* Provide a libusb device handle for the device
* Provide write and read callbacks for the actual transport of usbredir data
* Monitor for usbredir and libusb read/write events and call their handlers
"""

perl_compress_rpm_info = """Name        : perl-Compress-Raw-Zlib
Epoch       : 1
Version     : 2.061
Release     : 4.el7
Architecture: x86_64
Install Date: Sat Jan 26 20:05:50 2019
Group       : Development/Libraries
Size        : 139803
License     : GPL+ or Artistic
Signature   : RSA/SHA256, Fri Jul  4 04:15:33 2014, Key ID 24c6a8a7f4a80eb5
Source RPM  : perl-Compress-Raw-Zlib-2.061-4.el7.src.rpm
Build Date  : Tue Jun 10 01:12:08 2014
Build Host  : worker1.bsys.centos.org
Relocations : (not relocatable)
Packager    : CentOS BuildSystem <http://bugs.centos.org>
Vendor      : CentOS
URL         : http://search.cpan.org/dist/Compress-Raw-Zlib/
Summary     : Low-level interface to the zlib compression library
Description :
The Compress::Raw::Zlib module provides a Perl interface to the zlib
compression library, which is used by IO::Compress::Zlib.
Obsoletes   : 
"""  # noqa, PEP-8 disabled because of example output has trailing spaces
