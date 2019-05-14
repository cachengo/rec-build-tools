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

scriptdir="$(dirname $(readlink -f ${BASH_SOURCE[0]}))"
source $scriptdir/lib.sh

work=${1:-$WORKTMP/manifest-work}
work=$(readlink -f $work)
rm -rf $work
mkdir -p $work
cp -f $MANIFEST_PATH/*.spec $work

$scriptdir/create_mock_config.sh $BUILD_CONFIG_INI $work/mock_config

rpm_macros=$work/rpmmacros
$scriptdir/mock2rpmbuild_config.py --mock-config $work/mock_config/mock.cfg --output-file-path $rpm_macros

docker run --rm \
    -v $rpm_macros:/root/.rpmmacros \
    -v $work:/work \
    alpine:3.9.4 \
    sh -c '\
        apk add rpm && \
        rpmbuild --build-in-place --rmspec -ba /work/*.spec && \
        find /root/rpmbuild -name "*.rpm" | xargs -I "{}" mv {} /work'

_add_rpms_to_localrepo $(find $work -name '*.rpm')
