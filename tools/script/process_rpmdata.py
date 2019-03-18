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

from tools.convert import to_json, CsvConverter
from tools.log import set_logging
from tools.io import write_to, read_json


class RpmDataProcesser(object):
    def __init__(self, rpmdata):
        self.components = self._get_components(rpmdata)

    @staticmethod
    def _get_components(rpmdata):
        components = []
        bom_field_map = {'name': 'Name',
                         'version': 'Version',
                         'foss': 'FOSS',
                         'source-url': 'Source URL',
                         'crypto-capable': 'Crypto capable'}
        for rpm in rpmdata:
            components.append(unicode_recursively(rpm))
            bom = rpm['BOM']
            if bom:
                for material in bom:
                    component = {'Source RPM': rpm['Source RPM']}
                    for field in material:
                        component[bom_field_map[field]] = material[field]
                    components.append(unicode_recursively(component))
        return components

    def gen_components(self, path):
        write_to(path, to_json(self.components))

    def gen_components_csv(self, path):
        csv = CsvConverter(self.components,
                           preferred_field_order=['Name', 'Version', 'Release', 'Source RPM'])
        write_to(path, csv.convert_to_ms_excel(text_fields=['Version']))


def unicode_recursively(something):
    if isinstance(something, dict):
        return {unicode_recursively(key): unicode_recursively(value) for key, value in
                something.iteritems()}
    elif isinstance(something, list):
        return [unicode_recursively(element) for element in something]
    elif isinstance(something, unicode):
        return something.encode('utf-8')
    return something


def parse(args):
    p = argparse.ArgumentParser(
        description='Process rpmdata for multitude of tools',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    p.add_argument('--verbose', '-v', action='store_true',
                   help='More verbose logging')
    p.add_argument('--rpmdata-path', required=True,
                   help='RPM data json file path')
    p.add_argument('--output-components',
                   help='Component list that includes also RPM sub-components')
    p.add_argument('--output-components-csv',
                   help='Component list that includes also RPM sub-components as CSV')
    args = p.parse_args(args)
    return args


def main(input_args):
    args = parse(input_args)
    if args.verbose:
        set_logging(debug=True)
    else:
        set_logging(debug=False)
    p = RpmDataProcesser(read_json(args.rpmdata_path))
    if args.output_components:
        p.gen_components(args.output_components)
    if args.output_components_csv:
        p.gen_components_csv(args.output_components_csv)


if __name__ == "__main__":
    main(sys.argv[1:])
