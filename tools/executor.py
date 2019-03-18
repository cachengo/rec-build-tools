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
import logging
import shlex
import subprocess


class ExecutionError(Exception):
    def __init__(self, msg, result):
        super(ExecutionError, self).__init__(msg)
        self.result = result


class Result(object):
    def __init__(self, status, stdout, stderr):
        self.status = status
        self.stdout = stdout
        self.stderr = stderr

    @property
    def str_status(self):
        return 'Status:"{}"'.format(self.status)

    @property
    def str_stdout(self):
        return 'Stdout:"{}"'.format(self.stdout)

    @property
    def str_stderr(self):
        return 'Stderr:"{}"'.format(self.stderr)

    def __str__(self):
        return '\n'.join([self.str_status, self.str_stdout, self.str_stderr])


def run(*args, **kwargs):
    return Executor().run(*args, **kwargs)


class Executor(object):
    def __init__(self, shell=False, chdir=None):
        self.shell = shell
        self.chdir = chdir

    def run(self, cmd, raise_on_error=True, raise_on_stderr=True, retries=0):
        result = self._run(cmd, retries)
        if raise_on_error and result.status != 0:
            raise ExecutionError('Command "{}" execution status NOT zero: {}'.format(
                cmd, str(result)), result.status)
        if raise_on_stderr and result.stderr:
            raise ExecutionError('Command "{}" execution stderr not empty: {}'.format(
                cmd, str(result)), result.status)
        return result

    @staticmethod
    def _log_result(result):
        logging.debug('Result: %s', str(result))

    def _run(self, cmd, retries):
        logstr = 'Executing command: "{}"'.format(cmd)
        cwd = os.getcwd()
        if self.chdir is not None:
            os.chdir(self.chdir)
            logstr += ' in dir {}'.format(self.chdir)
        logging.debug(logstr)
        result = self._run_with_retries(cmd, retries)
        if self.chdir is not None:
            os.chdir(cwd)
        return result

    def _run_with_retries(self, cmd, retries):
        result = self._execute(cmd)
        while result.status != 0 and retries > 0:
            logging.debug('Retrying, retries left: %s', retries)
            retries -= 1
            result = self._execute(cmd)
            self._log_result(result)
            if result.status == 0:
                break
        return result

    def _execute(self, cmd):
        if not self.shell:
            if isinstance(cmd, list):
                cmd_args = cmd[:]
            else:
                cmd_args = shlex.split(cmd)
        else:
            cmd_args = cmd
        process = subprocess.Popen(cmd_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   shell=self.shell)
        stdout, stderr = process.communicate()
        result = Result(process.returncode, stdout, stderr)
        return result
