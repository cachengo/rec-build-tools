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
set -e
set -o pipefail

usage() {
    echo "Builds all git repositories under give search dirs"
    echo "Usage: $0 -m <manifest-dir> -w <work-dir> -r <rpmbuilder-dir> <rpm-create-search-dir> [<rpm-create-search-dir>..]"
    exit 1
}

while getopts "m:w:r:" OPT; do
    case $OPT in
    m)
        export MANIFEST_PATH=$(readlink -f $OPTARG)
        ;;
    w)
        export WORK=$OPTARG
        ;;
    r)
        export RPMBUILDER_PATH=$(readlink -f $OPTARG)
        ;;
    *)
        usage
        ;;
    esac
done

[ -z "$MANIFEST_PATH" ] && usage
[ -z "$RPMBUILDER_PATH" ] && usage
[ -z "$WORK" ] && usage

shift "$((OPTIND-1))"
search_paths="$@"
[ "$#" -eq 0 ] && usage
for p in $search_paths; do
    [ ! -d "$p" ] && usage
done

scriptdir="$(dirname $(readlink -f ${BASH_SOURCE[0]}))"
source $scriptdir/lib.sh

projects_to_build=$(find $search_paths -name .git -printf "%h\n" | sort)

work=$WORKTMP/rpms
rm -rf $work
mkdir -p $work

$scriptdir/create_mock_config.sh $BUILD_CONFIG_INI $work/mock_config

CENTOS_SOURCES="$(_read_build_config rpm centos_sources)" \
$RPMBUILDER_PATH/makebuild.py \
    -m $work/mock_config/mock.cfg \
    -w $work \
    $projects_to_build #-v --nowipe

echo "### Built RPMS #######################################"
find $work/projects/ -type f -name '*.rpm' | xargs ls -l
echo "### Built RPM details ##########################################"
for rpm in $(find $work/projects/ -type f -name '*.rpm'); do
    echo "=== $rpm ========================"
    rpm -qip $rpm
done

_add_rpms_to_localrepo $(find $work/buildrepository/mock -name '*.rpm')

