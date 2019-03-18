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

import pytest
import mock

from tools.releasereader import ReleaseReader
from tools.executor import Result


@pytest.mark.parametrize('curr_release, next_release', [
    ('ABC_D19-0', 'ABC_D19-1'),
    ('ABC_D19-19', 'ABC_D19-20'),
    ('ABC_D19A-1', 'ABC_D19A-2'),
    ('ABC_D19A-1.0', 'ABC_D19A-1.1'),
    ('ABC_D20-0', 'ABC_D20-1')
])
@mock.patch('tools.releasereader.Executor')
def test_next_release(mock_exec, curr_release, next_release):
    mock_exec.return_value.run.return_value = Result(0, curr_release + '\n', '')
    assert ReleaseReader('test-path').get_next_release_label() == next_release
    mock_exec.assert_called_once_with(chdir='test-path')
    mock_exec.return_value.run.assert_called_once_with(['git', 'describe', '--tags', '--abbrev=0'])
