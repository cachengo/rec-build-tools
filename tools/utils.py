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


def apply_jenkins_auth(url):
    validate_environ(['JENKINS_USERNAME', 'JENKINS_TOKEN'])
    protocol, address = url.split('://')
    url = '{protocol}://{user}:{token}@{address}'.format(**dict(protocol=protocol,
                                                                user=os.environ['JENKINS_USERNAME'],
                                                                token=os.environ['JENKINS_TOKEN'],
                                                                address=address))
    return url


def validate_environ(expected_vars):
    for env in expected_vars:
        if env not in os.environ:
            raise Exception('{} must be defined in environment'.format(env))
