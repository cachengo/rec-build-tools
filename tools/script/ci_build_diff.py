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

import logging
import sys
import argparse
from operator import itemgetter
from pprint import pformat

from tools.convert import CsvConverter
from tools.io import read_json, write_to, write_json
from tools.log import set_logging


class SwComponent(dict):

    @property
    def name(self):
        return self['Name']

    @property
    def version(self):
        return self['Version']

    @property
    def foss_id(self):
        return self.name, self.version, self.get('Release')

    def __str__(self):
        return '{}:{}({})'.format(self.name,
                                  self.version,
                                  self['Source RPM'])


class BuildDiffReader(object):

    def __init__(self):
        self.changes = {}
        self.summary = {}

    @staticmethod
    def get_component_names(data):
        return [i['Name'] for i in data]

    @staticmethod
    def get_components(name, components):
        out = []
        for component in components:
            if component['Name'] == name:
                out.append(SwComponent(component))
        return sorted(out, key=itemgetter('Name', 'Version', 'Source RPM'))

    def read(self, json_old, json_new):
        old_build = read_json(json_old)
        new_build = read_json(json_new)
        self.summary['input'] = {}
        self.summary['input']['from'] = len(old_build)
        self.summary['input']['to'] = len(new_build)
        self.changes = self.read_build_diff(old_build, new_build)
        self.summary['output'] = self._generate_summary(self.changes)

    @staticmethod
    def _generate_summary(changes):
        summary = {}
        summary['counts'] = changes['counts']
        summary['added'] = {name: [str(c) for c in compos] for name, compos in
                            changes['added'].items()}
        summary['removed'] = {name: [str(c) for c in compos] for name, compos in
                              changes['removed'].items()}
        summary['changed'] = {name: {'old': [str(c) for c in change['old']],
                                     'new': [str(c) for c in change['new']]} for name, change in
                              changes['changed'].items()}
        return summary

    def read_build_diff(self, old_build, new_build):
        old_names = self.get_component_names(old_build)
        logging.debug('Old names: {}'.format(old_names))
        new_names = self.get_component_names(new_build)
        logging.debug('New names: {}'.format(new_names))
        added = {n: self.get_components(n, new_build) for n in set(new_names) - set(old_names)}
        self._mark('[MARK] added', [j for i in added.values() for j in i])
        removed = {n: self.get_components(n, old_build) for n in set(old_names) - set(new_names)}
        self._mark('[MARK] removed', [j for i in removed.values() for j in i])
        changed = {}
        for n in set(old_names) & set(new_names):
            old_components = self.get_components(n, old_build)
            new_components = self.get_components(n, new_build)
            if sorted([i.foss_id for i in old_components]) != \
                    sorted([i.foss_id for i in new_components]):
                changed[n] = {'old': old_components, 'new': new_components}
                self._mark('[MARK] changed old', changed[n]['old'])
                self._mark('[MARK] changed new', changed[n]['new'])
        return dict(counts=dict(added=len(added),
                                changed=len(changed),
                                removed=len(removed)),
                    added=added,
                    removed=removed,
                    changed=changed)

    @staticmethod
    def _mark(title, components):
        logging.debug(
            '[MARK] {}: {}'.format(title, pformat([i.foss_id for i in components])))

    @staticmethod
    def _get_csv_cells(name, old_components, new_components):
        cells = dict(name=name)
        if old_components:
            cells.update(dict(old_components='\n'.join([str(i) for i in old_components]),
                              old_srpms='\n'.join([i['Source RPM'] for i in old_components]),
                              old_licenses='\n'.join(
                                  [i.get('License', 'Unknown') for i in old_components])))
        if new_components:
            cells.update(dict(new_components='\n'.join([str(i) for i in new_components]),
                              new_srpms='\n'.join([i['Source RPM'] for i in new_components]),
                              new_licenses='\n'.join(
                                  [i.get('License', 'Unknown') for i in new_components])))
        return cells

    def write_csv(self, path):
        data = []
        for name, components in self.changes['added'].items():
            data += [self._get_csv_cells(name, [], components)]

        for name, components in self.changes['removed'].items():
            data += [self._get_csv_cells(name, components, [])]

        for name, components in self.changes['changed'].items():
            data += [self._get_csv_cells(name, components['old'], components['new'])]

        csv = CsvConverter(sorted(data, key=itemgetter('name')),
                           preferred_field_order=['name',
                                                  'old_components', 'old_srpms', 'old_licenses',
                                                  'new_components', 'new_srpms', 'new_licenses'],
                           escape_newlines=False)
        write_to(path, csv.convert_to_ms_excel())


def parse(args):
    parser = argparse.ArgumentParser(description='Outputs RPM changes between two CI builds')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='More verbose logging')
    parser.add_argument('components_json_1',
                        help='Components json file path (CI build artifact)')
    parser.add_argument('components_json_2',
                        help='Components json file path (CI build artifact)')
    parser.add_argument('--output-json',
                        help='output to json file')
    parser.add_argument('--output-csv',
                        help='output to $MS csv file')
    return parser.parse_args(args)


def main(input_args):
    args = parse(input_args)
    set_logging(debug=args.verbose)
    x = BuildDiffReader()
    x.read(args.components_json_1, args.components_json_2)
    logging.info('----- SUMMARY ------\n{}'.format(pformat(x.summary)))
    if args.output_json:
        write_json(args.output_json, x.changes)
    if args.output_csv:
        x.write_csv(args.output_csv)


if __name__ == '__main__':
    main(sys.argv[1:])
