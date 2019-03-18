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

import sys

from tools.buildconfig import BuildConfigParser


def main():
    config = BuildConfigParser(sys.argv[1])
    if len(sys.argv) == 3:
        print(config.items(sys.argv[2]))
    elif len(sys.argv) == 4:
        print(config.get(sys.argv[2], sys.argv[3]))
    else:
        raise Exception('Invalid parameter count: {}'.format(len(sys.argv)))


if __name__ == "__main__":
    main()
