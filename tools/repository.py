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

from tools.buildconfig import BuildConfigParser
from tools.statics import BUILD_CONFIG_PATH
from tools.utils import validate_environ


class RepositoryConfig(object):
    def __init__(self, ini_file=BUILD_CONFIG_PATH):
        self.config = BuildConfigParser(ini_file=ini_file)

    def read_section(self, section):
        repositories = []
        for repo_name, repo_value in self.config.items(section):
            parts = repo_value.split('#')
            repodata = dict(name=repo_name, baseurl=parts[0])
            for p in parts[1:]:
                key, value = p.split('=', 1)
                repodata[key] = value
            repositories.append(repodata)
        return repositories

    def read_sections(self, sections):
        repositories = []
        for s in sections:
            repositories += self.read_section(s)
        return repositories

    @classmethod
    def get_localrepo(cls, remote=False):
        dirname = 'repo'
        if remote:
            validate_environ(['BUILD_URL'])
            baseurl = os.path.join(os.environ['BUILD_URL'], 'artifact/results', dirname)
        else:
            validate_environ(['WORK'])
            baseurl = 'file://' + \
                      os.path.join(os.environ['WORK'], 'results', dirname)
        return dict(name='localrepo', baseurl=baseurl)
