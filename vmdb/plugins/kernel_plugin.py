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



import logging
import sys

import cliapp

import vmdb


class KernelPlugin(cliapp.Plugin):

    def enable(self):
        self.app.step_runners.add(KernelStepRunner())
        

class KernelStepRunner(vmdb.StepRunnerInterface):

    def get_required_keys(self):
        return ['kernel']

    def run(self, step_spec, settings, state):
        package = step_spec['kernel']
        fstag = step_spec['fstag']
        mount_point = state.mounts[fstag]
        sys.stdout.write(
            'Install {} to filesystem at {} ({})\n'.format(
                package, mount_point, fstag))
        cliapp.runcmd(
            ['chroot', mount_point, 'apt', '-y', 'install', package],
            stdout=None, stderr=None)

