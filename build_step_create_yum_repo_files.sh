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

set -e

scriptdir="$(dirname $(readlink -f ${BASH_SOURCE[0]}))"
source $scriptdir/lib.sh

config_ini=${1:-$BUILD_CONFIG_INI}
output_dir=${2:-$REPO_FILES}
[ -f "$config_ini" ] || _abort "Config INI '$config_ini' not found"

gen() {
  PYTHONPATH=$LIBDIR python $LIBDIR/tools/script/generate_repo_files.py \
    --config-ini $config_ini \
    --output-dir $output_dir \
    $1
}

mkdir -p $output_dir

gen localrepo
gen repositories
gen baseimage-repositories
