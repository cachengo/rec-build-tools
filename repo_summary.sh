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

scriptdir="$(dirname $(readlink -f ${BASH_SOURCE[0]}))"
source $scriptdir/lib.sh

_run_repo_cmd()
{
  _divider
  _run_cmd $@
}

pushd $WORK/.repo/repo
_run_repo_cmd git rev-parse --short HEAD
popd
echo q | _run_repo_cmd repo info
_run_repo_cmd repo status -o
echo q | _run_repo_cmd repo forall -p -c git rev-parse HEAD

# Store build manifest with project HEADS to a file
repo manifest -o $WORKRESULTS/manifest.xml
repo manifest -r -o $WORKRESULTS/manifest_revisions.xml
