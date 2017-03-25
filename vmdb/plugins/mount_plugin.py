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
import os
import sys
import tempfile

import cliapp

import vmdb


class MountPlugin(cliapp.Plugin):

    def enable(self):
        self.app.step_runners.add(MountStepRunner())
        

class MountStepRunner(vmdb.StepRunnerInterface):

    def get_required_keys(self):
        return ['mount', 'tag']

    def run(self, step_spec, settings, state):
        if not hasattr(state, 'mounts'):
            state.mounts = {}

        device = step_spec['mount']
        tag = step_spec['tag']
        if tag in state.mounts:
            raise Exception('mount tag {} already used'.format(tag))

        mount_point = tempfile.mkdtemp()
        sys.stdout.write(
            'Mounting {} ({}) on {}\n'.format(device, tag, mount_point))
        cliapp.runcmd(['mount', device, mount_point])
        state.mounts[tag] = mount_point

    def teardown(self, step_spec, settings, state):
        device = step_spec['mount']
        tag = step_spec['tag']
        mount_point = state.mounts[tag]
        
        sys.stdout.write(
            'Unmounting {} ({}) from {}\n'.format(mount_point, tag, device))
        cliapp.runcmd(['umount', mount_point])
        os.rmdir(mount_point)
