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

set -eu

NEXUS_URL=$1
NEXUS_REPOSITORY=$2
NEXUS_REPOSITORY_BASE_PATH=$3
shift;shift;shift
NEXUS_REPOSITORY_SEARCH_PATTERNS=$@

_abort() {
  echo "ERROR: $@"
  exit 1
}

_search_group() {
  local params=""
  [ -n "$1" ] && params+="&group=$1"
  [ -n "${2:-}" ] && params+="&name=$2"
  curl "${NEXUS_URL}/service/rest/v1/search?repository=${NEXUS_REPOSITORY}${params}"
}

for pat in $NEXUS_REPOSITORY_SEARCH_PATTERNS; do
  search_group="/$NEXUS_REPOSITORY_BASE_PATH/$(echo $pat | cut -d':' -f1)"
  search_name=""
  if echo $pat | grep ':'; then
      search_name="$(echo $pat | cut -d':' -f2)"
  fi
  resp=$(_search_group $search_group $search_name)
  if [ "$(echo $resp | jq -r '.continuationToken')" != "null" ]; then
    _abort "Pagination not implemented"
  fi
  for url in $(echo $resp | jq -r '.items[].assets[].downloadUrl'); do
    to=${url#$NEXUS_URL/repository/$NEXUS_REPOSITORY/$NEXUS_REPOSITORY_BASE_PATH/}
    mkdir -p $(dirname $to)
    echo "Fetch $url"
    curl $url > $to
  done
done
