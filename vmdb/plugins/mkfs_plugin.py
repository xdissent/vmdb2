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


class MkfsPlugin(cliapp.Plugin):

    def enable(self):
        self.app.step_runners.add(MkfsStepRunner())
        

class MkfsStepRunner(vmdb.StepRunnerInterface):

    def get_required_keys(self):
        return ['mkfs', 'partition']

    def run(self, step_spec, settings, state):
        fstype = step_spec['mkfs']
        part_tag = step_spec['partition']
        device = state.parts[part_tag]
        sys.stdout.write(
            'Creating {} filesystem on {}\n'.format(fstype, device))
        cliapp.runcmd(['/sbin/mkfs', '-t', fstype, device])
