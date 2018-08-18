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
import stat

import cliapp

import vmdb


class PartitionPlugin(cliapp.Plugin):

    def enable(self):
        self.app.step_runners.add(MklabelStepRunner())
        self.app.step_runners.add(MkpartStepRunner())


class MklabelStepRunner(vmdb.StepRunnerInterface):

    def get_required_keys(self):
        return ['mklabel']

    def run(self, step, settings, state):
        label_type = step['mklabel']
        device = step['device']
        vmdb.progress(
            'Creating partition table ({}) on {}'.format(label_type, device))
        vmdb.runcmd(['parted', '-s', device, 'mklabel', label_type])
        state.parts = {}


class MkpartStepRunner(vmdb.StepRunnerInterface):

    def get_required_keys(self):
        return ['mkpart']

    def run(self, step, settings, state):
        part_type = step['mkpart']
        device = step['device']
        start = step['start']
        end = step['end']
        part_tag = step['part-tag']
        fs_type = step.get('fs-type', 'ext2')

        vmdb.progress(
            'Creating partition ({}) on {} ({} to {})'.format(
                part_type, device, start, end))

        orig = self.list_partitions(device)
        vmdb.runcmd(['parted', '-s', device, 'mkpart', part_type, fs_type, start, end])
        new = self.list_partitions(device)
        diff = self.diff_partitions(orig, new)
        print('diff:', diff)
        assert len(diff) == 1

        if self.is_block_dev(device):
            self.remember_partition(state, diff[0], part_tag)
        else:
            part_dev = self.create_loop_dev(device)
            assert part_dev is not None
            self.remember_partition(state, part_dev, part_tag)

    def is_block_dev(self, filename):
        st = os.lstat(filename)
        return stat.S_ISBLK(st.st_mode)

    def list_partitions(self, device):
        output = vmdb.runcmd(['parted', '-m', device, 'print'])
        output = output.decode('UTF-8')
        partitions = [
            line.split(':')[0]
            for line in output.splitlines()
            if ':' in line
        ]
        return [
            word if word.startswith('/') else '{}{}'.format(device, word)
            for word in partitions
        ]

    def diff_partitions(self, old, new):
        return [
            line
            for line in new
            if line not in old
        ]

    def remember_partition(self, state, part_dev, part_tag):
        print('remembering partition', part_dev, 'as', part_tag)
        parts = getattr(state, 'parts', {})
        parts[part_tag] = part_dev
        state.parts = parts

    def create_loop_dev(self, device):
        vmdb.runcmd(['kpartx', '-dsv', device])
        output = vmdb.runcmd(['kpartx', '-asv', device]).decode('UTF-8')
        device_file = None
        for line in output.splitlines():
            words = line.split()
            if words[0] == 'add':
                name = words[2]
                return '/dev/mapper/{}'.format(name)
        return None

    def teardown(self, step, settings, state):
        device = step['device']
        vmdb.progress(
            'Undoing loopback devices for partitions on {}'.format(device))
        vmdb.runcmd(['kpartx', '-dsv', device])
