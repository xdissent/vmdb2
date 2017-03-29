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
        sys.stdout.write(
            'Creating partition table ({}) on {}\n'.format(label_type, device))
        cliapp.runcmd(['parted', device, 'mklabel', label_type], stderr=None)
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

        sys.stdout.write(
            'Creating partition ({}) on {} ({} to {})\n'.format(
                part_type, device, start, end))
        cliapp.runcmd(['parted', '-s', device, 'mkpart', part_type, start, end])

        cliapp.runcmd(['kpartx', '-d', device])
        output = cliapp.runcmd(['kpartx', '-asv', device])
        for line in output.splitlines():
            words = line.split()
            if words[0] == 'add':
                name = words[2]
                device_file = '/dev/mapper/{}'.format(name)

        parts = getattr(state, 'parts', {})
        parts[part_tag] = device_file
        state.parts = parts

    def teardown(self, step, settings, state):
        device = step['device']
        sys.stdout.write(
            'Undoing loopback devices for partitions on {}\n'.format(device))
        cliapp.runcmd(['kpartx', '-d', device])
