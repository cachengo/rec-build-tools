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

scriptdir="$(dirname $(readlink -f ${BASH_SOURCE[0]}))"
source $scriptdir/lib.sh

_get_projects_all() { repo list -g torpm -n | sort; }

_get_project_dirs() {
  for i in $@; do
    repo info -l $i | grep "^Mount path: " | awk '{print $3}' | tr '\n' ' '
  done
}

build_rpms()
{
  local work=$1
  shift
  rm -rf $work
  mkdir -p $work

  CENTOS_SOURCES="$(_read_build_config rpm centos_sources)" \
  $RPM_BUILDER/makebuild.py \
    -m $RPM_BUILDER_SETTINGS \
    -w $work \
    $@ #-v --nowipe
}

# build one or all projects
if [ -n "$1" ]; then
  projects_to_build=$@
else
  projects_to_build="$MANIFEST_PATH $(_get_project_dirs $(_get_projects_all))"
  _run_cmd $LIBDIR/prepare_manifest.sh
fi

rpmwork=$WORKTMP/rpms
build_rpms $rpmwork $projects_to_build
_add_rpms_to_repos_from_workdir $rpmwork
