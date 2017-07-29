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
        self.mount_rootfs(step, settings, state)

    def teardown(self, step, settings, state):
        self.unmount_rootfs(step, settings, state)

    def mount_rootfs(self, step, settings, state):
        if not hasattr(state, 'mounts'):
            state.mounts = {}

        part_tag = step['mount']
        fs_tag = step['fs-tag']
        dirname = step.get('dirname')
        mount_on = step.get('mount-on')

        if fs_tag in state.mounts:
            raise Exception('fs-tag {} already used'.format(fs_tag))

        if dirname:
            if not mount_on:
                raise Exception('no mount-on tag given')

            if mount_on not in state.mounts:
                raise Exception('cannot find tag {}'.format(mount_on))

            mount_point = os.path.join(
                state.mounts[mount_on], './' + step['dirname'])

            if not os.path.exists(mount_point):
                os.makedirs(mount_point)
        else:
            mount_point = tempfile.mkdtemp()

        device = state.parts[part_tag]

        vmdb.runcmd(['mount', device, mount_point])
        state.mounts[fs_tag] = mount_point

        return mount_point

    def unmount_rootfs(self, step, settings, state):
        fs_tag = step['fs-tag']
        mount_point = state.mounts[fs_tag]

        vmdb.runcmd(['umount', mount_point])
        os.rmdir(mount_point)
