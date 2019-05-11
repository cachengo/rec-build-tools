#!/bin/bash
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

set -x
set -eu

usage() {
    echo "Usage: $0 -m <manifest-path> -w <work-dir-path>"
    exit 1
}

[ "$#" -ne 4 ] && usage
while getopts "m:w:" OPT; do
    case $OPT in
    m)
        export MANIFEST_PATH=$(readlink -f $OPTARG)
        ;;
    w)
        export WORK=$OPTARG
        ;;
    *)
        usage
        ;;
    esac
done

scriptdir="$(dirname $(readlink -f ${BASH_SOURCE[0]}))"
source $scriptdir/lib.sh

_initialize_work_dirs

# Create manifest RPM
$LIBDIR/create_manifest_rpm.sh

# Create repo config
$LIBDIR/build_step_create_yum_repo_files.sh

# QCOW
$LIBDIR/build_step_golden_image.sh
sha1short=$(grep -v product-manifest $RPMLISTS/rpmlist | sha1sum | cut -c-8)

# ISO images
$LIBDIR/build_step_create_install_cd.sh

echo "=== SUCCESS ==="
echo "Build results are in $WORKRESULTS"
echo "Installed RPMS checksum: ${sha1short} (this will change if list of installed RPMs changes)"
