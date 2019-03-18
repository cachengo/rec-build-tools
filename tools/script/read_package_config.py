#!/usr/bin/env python
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

import argparse
import sys

from tools.package import PackageConfigReader


def parse(args):
    p = argparse.ArgumentParser(
        description='Read package configuration',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    p.add_argument('--config', required=False, help='Package YAML config file path')
    p.add_argument('--separator', required=False, default=' ',
                   help='Separator for the resulting stdout list')
    p.add_argument('package_operation_type', choices=['install', 'uninstall'],
                   help='list packages by operation type')
    args = p.parse_args(args)
    return args


def main(input_args):
    args = parse(input_args)
    kwargs = {}
    if args.config is not None:
        kwargs['config_file'] = args.config
    print(args.separator.join(PackageConfigReader(**kwargs).get(args.package_operation_type)))


if __name__ == "__main__":
    main(sys.argv[1:])
