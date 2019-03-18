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
import re
import logging

from tools.executor import run
from tools.rpm import RpmData


class YumRpm(RpmData):
    @property
    def arch(self):
        return self['Arch']


class YumInfoParserException(BaseException):
    pass


class YumDownloaderException(BaseException):
    def __init__(self, msg, failed_packages):
        super(YumDownloaderException, self).__init__()
        self.msg = msg
        self.failed_packages = failed_packages

    def __str__(self):
        return self.msg


class YumInfoParser(object):
    """
    Parse 'yum info' output
    """

    def parse_file(self, yum_info_installed_file_path):
        with open(yum_info_installed_file_path, 'r') as f:
            return self.parse_installed(f.read())

    def parse_installed(self, yum_info_installed):
        return self._parse_rpms_with_regexp(yum_info_installed, r'\nInstalled Packages\n')

    def parse_available(self, yum_info_installed):
        return self._parse_rpms_with_regexp(yum_info_installed, r'Available Packages\n')

    def _parse_rpms_with_regexp(self, yum_output, regexp):
        parsed_output = self._split_yum_output_with(yum_output, regexp)
        return [self.parse_package(pkg) for pkg in parsed_output[1].split('\n\n') if pkg]

    @staticmethod
    def _split_yum_output_with(output, regexp):
        parsed_output = re.split(regexp, output)
        if len(parsed_output) != 2:
            raise YumInfoParserException(
                '{} not found from output: {}'.format(repr(regexp), output[:1000]))
        return parsed_output

    @staticmethod
    def parse_package(yum_info_output):
        result = YumRpm()
        current_key = None
        for line in re.findall(r'^(.+?) : (.*)$', yum_info_output, re.MULTILINE):
            parsed_key = line[0].strip()
            parsed_value = line[1].rstrip(' ')
            if parsed_key:
                result[parsed_key] = parsed_value
                current_key = parsed_key
            elif current_key in ['License', 'Summary']:
                result[current_key] = result[current_key] + ' ' + parsed_value
            else:
                result[current_key] = result[current_key] + '\n' + parsed_value
        return result


class Yum(object):
    def __init__(self):
        self.config = YumConfig(filename='tmp_yum.conf')

    @classmethod
    def clean_and_remove_cache(cls):
        cls.clean_all()
        cls.remove_cache_dir()

    @classmethod
    def clean_all(cls):
        run(['yum', 'clean', 'all'], raise_on_stderr=False)

    @classmethod
    def remove_cache_dir(cls):
        run(['rm', '-rf', '/var/cache/yum'], raise_on_stderr=True)

    @classmethod
    def read_available_pkgs(cls, name, url):
        filename = 'tmp_yum.conf'
        yum_tmp_conf = YumConfig()
        yum_tmp_conf.add_repository(name, url)
        with open(filename, 'w') as f:
            f.write(yum_tmp_conf.render())
        cmd = ['yum',
               '--config={}'.format(filename),
               '--showduplicates',
               '--setopt=keepcache=0',
               '--disablerepo=*',
               '--enablerepo={}'.format(name),
               'info',
               'available']
        return run(cmd, raise_on_stderr=False).stdout

    def add_repo(self, name, url):
        self.config.add_repository(name, url)

    def read_all_packages(self):
        self.config.write()
        logging.debug('Yum config:\n{}'.format(self.config))
        cmd = ['yum',
               '--config={}'.format(self.config.filename),
               '--showduplicates',
               '--setopt=keepcache=0',
               '--enablerepo=*',
               'info',
               'available']
        return run(cmd, raise_on_stderr=False).stdout


class YumDownloader(object):
    def download(self, rpms, repositories, to_dir=None, source=False):
        logging.debug('Downloading {} RPMs from repositories: {}'.format(len(rpms),
                                                                         [r['name'] for r in
                                                                          repositories]))
        result = self._download(rpms, repositories, to_dir=to_dir, source=source)
        downloaded_rpms = [rpm.rstrip('.rpm') for rpm in os.listdir(to_dir)]
        not_downloaded_rpms = [rpm for rpm in rpms if rpm not in downloaded_rpms]
        if len(rpms) != len(downloaded_rpms):
            logging.debug('Downloaded {}/{} RPMs: {}'.format(len(downloaded_rpms), len(rpms),
                                                             downloaded_rpms))
            # Not precise way to list not downloaded RPMs - RPM name may not match the metadata
            # We should read "rpm -qip" for each rpm and parse it
            raise YumDownloaderException(
                'Failed to download {}/{} RPMs: {}.\nYumdownloader result: {}'.format(
                    len(not_downloaded_rpms), len(rpms), not_downloaded_rpms, str(result)),
                not_downloaded_rpms
            )

    @staticmethod
    def _download(rpms, repositories, to_dir=None, source=False):
        filename = 'tmp_yum.conf'
        yum_tmp_conf = YumConfig()
        for r in repositories:
            yum_tmp_conf.add_repository(r['name'], r['baseurl'])
        with open(filename, 'w') as f:
            f.write(yum_tmp_conf.render())
        logging.debug('Downloading RPMs: {}'.format(rpms))
        cmd = ['yumdownloader']
        if to_dir is not None:
            cmd += ['--destdir={}'.format(to_dir)]
        cmd += ['--config={}'.format(filename),
                '--disablerepo=*',
                '--enablerepo={}'.format(','.join([r['name'] for r in repositories])),
                '--showduplicates']
        if source:
            cmd.append('--source')
        cmd += rpms
        return run(cmd, raise_on_stderr=False)


class YumConfig(object):
    def __init__(self, filename=None):
        self.filename = filename
        self.config = ['[main]',
                       '#cachedir=/var/cache/yum/$basearch/$releasever',
                       'reposdir=/foo/bar/xyz',
                       'keepcache=0',
                       'debuglevel=2',
                       '#logfile=/var/log/yum.log',
                       'exactarch=1',
                       'obsoletes=1',
                       'gpgcheck=0',
                       'plugins=1',
                       'installonly_limit=5',
                       'override_install_langs=en_US.UTF-8',
                       'tsflags=nodocs']
        self.repositories = []

    def add_repository(self, name, url, exclude=None):
        repo = ['[{}]'.format(name),
                'name = ' + name,
                'baseurl = ' + url,
                'enabled = 1',
                'gpgcheck = 0']
        if exclude is not None:
            repo.append('exclude = ' + exclude)
        self.repositories.append(repo)

    def __str__(self):
        return self.render()

    def render(self):
        blocks = ['\n'.join(self.config)] + ['\n'.join(repo) for repo in self.repositories]
        return '\n\n'.join(blocks)

    def write(self):
        with open(self.filename, 'w') as f:
            f.write(self.render())
