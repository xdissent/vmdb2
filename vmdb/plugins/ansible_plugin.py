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


class AnsiblePlugin(cliapp.Plugin):

    def enable(self):
        self.app.step_runners.add(AnsibleStepRunner())


class AnsibleStepRunner(vmdb.StepRunnerInterface):

    def get_required_keys(self):
        return ['ansible', 'playbook']

    def run(self, step, settings, state):
        fstag = step['ansible']
        playbook = step['playbook']
        mount_point = state.mounts[fstag]

        vmdb.progress(
            'Running ansible playbook {} on filesystem at {} ({})'.format(
                playbook, mount_point, fstag))

        state.ansible_inventory = self.create_inventory(mount_point)
        vmdb.progress(
            'Created {} for Ansible inventory'.format(state.ansible_inventory))
        vmdb.runcmd(
            ['ansible-playbook', '-c', 'chroot',
             '-i', state.ansible_inventory, playbook])

    def teardown(self, step, settings, state):
        if hasattr(state, 'ansible_inventory'):
            vmdb.progress('Removing {}'.format(state.ansible_inventory))
            os.remove(state.ansible_inventory)

    def create_inventory(self, chroot):
        fd, filename = tempfile.mkstemp()
        os.write(fd, '[image]\n{}\n'.format(chroot))
        os.close(fd)
        return filename
