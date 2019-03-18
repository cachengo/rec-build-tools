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

import os
import sys
import argparse
import logging

from tools.buildconfig import BuildConfigParser


def _parse(args):
    parser = argparse.ArgumentParser(description='Generate repo files from config ini sections')
    parser.add_argument('config_sections', metavar='config_section', nargs='+',
                        help='Config ini section')
    parser.add_argument('--output-dir', '-d', required=True,
                        help='Directory to output the repo files')
    parser.add_argument('--config-ini', '-c', required=True,
                        help='Path to the config ini to read')
    args = parser.parse_args(args)
    return args


class RepoGen(object):

    def __init__(self, output_dir, config_ini, config_sections):
        self.output_dir = output_dir
        self.config_sections = config_sections
        self.config = BuildConfigParser(ini_file=config_ini)

    def run(self):
        for section in self.config_sections:
            repo_file_path = os.path.join(self.output_dir, section + '.repo')
            self._write_repo_file(section, repo_file_path)

    def _write_repo_file(self, section, repo_file_path):
        with open(repo_file_path, 'w') as f:
            for repo in self.config.items(section):
                name = repo[0]
                parts = repo[1].split('#')
                url = parts[0]
                f.write('[%s]\n' % name)
                f.write('name=%s\n' % name)
                f.write('baseurl=%s\n' % url)
                f.write('enabled=1\n')
                f.write('gpgcheck=0\n')
                for part in parts[1:]:
                    f.write('%s\n' % part)
                f.write('\n')
        if os.path.getsize(repo_file_path) == 0:
            logging.error('Zero size output: {}'.format(repo_file_path))
            sys.exit(1)
        logging.info('Wrote repo: {}'.format(repo_file_path))


def main(input_args):
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    args = _parse(input_args)
    RepoGen(args.output_dir, args.config_ini, args.config_sections).run()


if __name__ == "__main__":
    main(sys.argv[1:])
