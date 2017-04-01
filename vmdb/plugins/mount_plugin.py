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
        return ['mount', 'fs-tag']

    def run(self, step, settings, state):
        if not hasattr(state, 'mounts'):
            state.mounts = {}

        part_tag = step['mount']
        fs_tag = step['fs-tag']
        if fs_tag in state.mounts:
            raise Exception('fs-tag {} already used'.format(fs_tag))

        device = state.parts[part_tag]
        mount_point = tempfile.mkdtemp()

        sys.stdout.write(
            'Mounting {} ({}) on {}\n'.format(device, fs_tag, mount_point))
        vmdb.runcmd(['mount', device, mount_point])
        state.mounts[fs_tag] = mount_point

    def teardown(self, step, settings, state):
        part_tag = step['mount']
        device = state.parts[part_tag]
        fs_tag = step['fs-tag']
        mount_point = state.mounts[fs_tag]
        
        sys.stdout.write(
            'Unmounting {} ({}) from {}\n'.format(mount_point, fs_tag, device))
        vmdb.runcmd(['umount', mount_point])
        os.rmdir(mount_point)
