# Copyright 2017  Lars Wirzenius
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# =*= License: GPL-3+ =*=



import os

import cliapp

import vmdb


class RootFSCachePlugin(cliapp.Plugin):

    def enable(self):
        self.app.settings.string(
            ['rootfs-tarball'],
            'store rootfs cache tar archives in FILE',
            metavar='FILE')

        self.app.step_runners.add(MakeCacheStepRunner())
        self.app.step_runners.add(UnpackCacheStepRunner())


class MakeCacheStepRunner(vmdb.StepRunnerInterface):

    def get_required_keys(self):
        return ['cache-rootfs']

    def run(self, step, settings, state):
        fs_tag = step['cache-rootfs']
        rootdir = state.mounts[fs_tag]
        tar_path = settings['rootfs-tarball']
        opts = step.get('options', '--one-file-system').split()
        if not tar_path:
            raise Exception('--rootfs-tarball MUST be set')
        if not os.path.exists(tar_path):
            vmdb.progress(
                'Caching contents of {} to {}'.format(rootdir, tar_path))
            vmdb.runcmd(['tar'] + opts + ['-C', rootdir, '-caf', tar_path, '.'])


class UnpackCacheStepRunner(vmdb.StepRunnerInterface):

    def get_required_keys(self):
        return ['unpack-rootfs']

    def run(self, step, settings, state):
        fs_tag = step['unpack-rootfs']
        rootdir = state.mounts[fs_tag]
        tar_path = settings['rootfs-tarball']
        if not tar_path:
            raise Exception('--rootfs-tarball MUST be set')
        if os.path.exists(tar_path):
            vmdb.progress(
                'Unpacking rootfs from {} to {}'.format(tar_path, rootdir))
            vmdb.runcmd(
                ['tar', '-C', rootdir, '-xf', tar_path, '--numeric-owner'])
            state.rootfs_unpacked = True
