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

set -o pipefail
set -e

LIBDIR="$(dirname $(readlink -f ${BASH_SOURCE[0]}))"

GOLDEN_BASE_IMAGE_FETCH_USER=${GOLDEN_BASE_IMAGE_FETCH_USER:-}
GOLDEN_BASE_IMAGE_FETCH_PASSWORD=${GOLDEN_BASE_IMAGE_FETCH_PASSWORD:-}

WORK=$(readlink -f ${WORK:-$(dirname $(dirname $LIBDIR))})
mkdir -p $WORK

WORKTMP=$WORK/tmp
WORKLOGS=$WORKTMP/logs
DURATION_LOG=$WORKLOGS/durations.log
MANIFEST_PATH=$(readlink -f ${MANIFEST_PATH:-$WORK/.repo/manifests})
BUILD_CONFIG_INI=${BUILD_CONFIG_INI:-$MANIFEST_PATH/build_config.ini}
GOLDEN_IMAGE_NAME=guest-image.img
TMP_GOLDEN_IMAGE=$WORKTMP/$GOLDEN_IMAGE_NAME

WORKRESULTS=$WORK/results
REPO_FILES=$WORKRESULTS/repo_files
REPO_DIR=$WORKRESULTS/repo
SRC_REPO_DIR=$WORKRESULTS/src_repo
RPMLISTS=$WORKRESULTS/rpmlists
CHECKSUM_DIR=$WORKRESULTS/bin_checksum
RESULT_IMAGES_DIR=$WORKRESULTS/images

function _read_build_config()
{
  local config_ini=$BUILD_CONFIG_INI
  if [[ -f "$1" ]] && [[ $1 == *.ini ]]; then
    config_ini=$1
    shift
  fi
  PYTHONPATH=$LIBDIR $LIBDIR/tools/script/read_build_config.py $config_ini $@
}

function _read_manifest_vars()
{
  PRODUCT_RELEASE_BUILD_ID="${BUILD_NUMBER:-0}"
  PRODUCT_RELEASE_LABEL="$(_read_build_config DEFAULT product_release_label)"
}

function _initialize_work_dirs()
{
  mkdir -p $WORK
  rm -rf $WORKRESULTS
  mkdir -p $WORKRESULTS $REPO_FILES $REPO_DIR $SRC_REPO_DIR $RPMLISTS $CHECKSUM_DIR
  # dont clear tmp, can be used for caching
  mkdir -p $WORKTMP
  rm -rf $WORKLOGS
  mkdir -p $WORKLOGS
}

function _log()
{
  echo "$(date) $@"
}

function _info()
{
  _log INFO: $@
}

function _header()
{
  _info "##################################################################"
  _info "# $@"
  _info "##################################################################"
}


function _divider()
{
  _info "------------------------------------------------------------------"
}


function _step()
{
  _header "STEP START: $@"
}


function _abort()
{
  _header "ERROR: $@"
  exit 1
}


function _success()
{
  _header "STEP OK: $@"
}

function _add_rpms_to_localrepo()
{
  local rpms=$@
  mkdir -p $REPO_DIR
  mkdir -p $SRC_REPO_DIR
  for rpm in $@; do
    if grep ".src.rpm" <<< "$rpm"; then
      cp -f $rpm $SRC_REPO_DIR
    else
      cp -f $rpm $REPO_DIR
    fi
  done
  _create_localrepo
}

function _create_localrepo()
{
  pushd $REPO_DIR
  createrepo --workers=8 --update .
  popd
  pushd $SRC_REPO_DIR
  createrepo --workers=8 --update .
  popd
}

function _publish_results()
{
  local from=$1
  local to=$2
  mkdir -p $(dirname $to)
  mv -f $from $to
}

function _publish_image()
{
  _publish_results $1 $2
  _create_checksum $2
}

function _create_checksum()
{
  _create_md5_checksum $1
  _create_sha256_checksum $1
}

function _create_sha256_checksum()
{
  pushd $(dirname $1)
    time sha256sum $(basename $1) > $(basename $1).sha256
  popd
}

function _create_md5_checksum()
{
  pushd $(dirname $1)
    time md5sum $(basename $1) > $(basename $1).md5
  popd
}

function _is_true()
{
  # e.g. for Jenkins boolean parameters
  [ "$1" == "true" ]
}

function _join_array()
{
  local IFS="$1"
  shift
  echo "$*"
}

function _get_package_list()
{
  PYTHONPATH=$LIBDIR $LIBDIR/tools/script/read_package_config.py $@
}

function _load_docker_image()
{
  local docker_image=$1
  if docker inspect ${docker_image} &> /dev/null; then
    echo "Using already built ${docker_image} image"
  else
    echo "Loading ${docker_image} image"
    local docker_image_url="$(_read_build_config DEFAULT docker_images)/${docker_image}.tar"
    curl -L $docker_image_url | docker load
  fi
}

