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

import json
import logging

from tools.convert import to_json


def write_to(file_path, data):
    with open(file_path, 'w') as f:
        f.write(data)
    logging.debug('Wrote: {}'.format(file_path))


def read_from(file_path):
    with open(file_path, 'r') as f:
        return f.read()


def write_json(file_path, data):
    write_to(file_path, to_json(data))


def read_json(file_path):
    return json.loads(read_from(file_path))
