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


class DebootstrapPlugin(cliapp.Plugin):

    def enable(self):
        self.app.step_runners.add(DebootstrapStepRunner())
        

class DebootstrapStepRunner(vmdb.StepRunnerInterface):

    def get_required_keys(self):
        return ['debootstrap', 'target', 'mirror']

    def run(self, step, settings, state):
        suite = step['debootstrap']
        tag = step['target']
        target = state.mounts[tag]
        mirror = step['mirror']
        if not (suite and tag and target and mirror):
            raise Exception('missing arg for debootstrap step')
        sys.stdout.write(
            'Debootstrap {} {} {}\n'.format(suite, target, mirror))
        cliapp.runcmd(['debootstrap', suite, target, mirror], stdout=None, stderr=None)