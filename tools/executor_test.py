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

from tools.executor import Executor, ExecutionError
from tools.executor import Result


@mock.patch.object(Executor, '_execute')
def test_success(mocky):
    mocky.side_effect = [Result(0, 'fake-stdout', '')]
    Executor().run('test-cmd')
    mocky.assert_called_once_with('test-cmd')


@mock.patch.object(Executor, '_execute')
def test_fail_returncode(mocky):
    mocky.side_effect = [Result(1, 'fake-stdout', '')]
    with pytest.raises(ExecutionError, match=r'execution status NOT zero'):
        Executor().run('test-cmd')
    mocky.assert_called_once_with('test-cmd')


@mock.patch.object(Executor, '_execute')
def test_fail_stderr(mocky):
    mocky.side_effect = [Result(0, 'fake-stdout', 'fake-stderr')]
    with pytest.raises(ExecutionError, match=r'stderr not empty'):
        Executor().run('test-cmd')
    mocky.assert_called_once_with('test-cmd')


@mock.patch.object(Executor, '_execute')
def test_success_ignore_returncode(mocky):
    mocky.side_effect = [Result(1, 'fake-stdout', '')]
    Executor().run('test-cmd', raise_on_error=False)
    mocky.assert_called_once_with('test-cmd')


@mock.patch.object(Executor, '_execute')
def test_success_ignore_stderr(mocky):
    mocky.side_effect = [Result(0, 'fake-stdout', 'fake-stderr')]
    Executor().run('test-cmd', raise_on_stderr=False)
    mocky.assert_called_once_with('test-cmd')


@mock.patch.object(Executor, '_execute')
def test_no_retry_on_success(mocky):
    mocky.side_effect = [Result(0, 'fake-stdout', '')]
    Executor().run('test-cmd', retries=1)
    mocky.assert_called_once_with('test-cmd')


@mock.patch.object(Executor, '_execute')
def test_retry_on_fail(mocky):
    mocky.side_effect = [Result(1, 'fake-stdout', ''),
                         Result(0, 'fake-stdout', '')]
    Executor().run('test-cmd', retries=1)
    expected = [mock.call('test-cmd'),
                mock.call('test-cmd')]
    assert mocky.mock_calls == expected


@mock.patch.object(Executor, '_execute')
def test_error_on_retry_exceeded(mocky):
    mocky.side_effect = [Result(1, 'fake-stdout', ''),
                         Result(1, 'fake-stdout', '')]
    with pytest.raises(ExecutionError):
        Executor().run('test-cmd', retries=1)
