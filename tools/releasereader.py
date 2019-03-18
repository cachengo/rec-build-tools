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

import re

from tools.executor import Executor


class ReleaseReader(object):
    def __init__(self, manifest_dir):
        self.manifest_dir = manifest_dir

    def read_current_release(self):
        return Executor(chdir=self.manifest_dir).run(
            ["git", "describe", "--tags", "--abbrev=0"]).stdout

    def get_next_release_label(self):
        current = self.read_current_release()
        match = re.search(r'^(.+[\.-])(\d+)$', current)
        return '{}{}'.format(match.group(1), (int(match.group(2)) + 1))
