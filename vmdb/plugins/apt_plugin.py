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


class AptPlugin(cliapp.Plugin):

    def enable(self):
        self.app.step_runners.add(AptStepRunner())


class AptStepRunner(vmdb.StepRunnerInterface):

    def get_required_keys(self):
        return ['apt', 'fs-tag']

    def run(self, step, settings, state):
        package = step['apt']
        fstag = step['fs-tag']
        mount_point = state.mounts[fstag]

        if not self.got_eatmydata(state):
            self.install_package(mount_point, [], 'eatmydata')
            state.got_eatmydata = True
        self.install_package(mount_point, ['eatmydata'], package)

    def got_eatmydata(self, state):
        return hasattr(state, 'got_eatmydata') and getattr(state, 'got_eatmydata')

    def install_package(self, mount_point, argv_prefix, package):
        env = os.environ.copy()
        env['DEBIAN_FRONTEND'] = 'noninteractive'

        vmdb.runcmd(
            ['chroot', mount_point] +
            argv_prefix +
            ['apt-get', '-y', '--no-show-progress', 'install', package],
            env=env)
