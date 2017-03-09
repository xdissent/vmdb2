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

import yaml

import vmdb


class Vmdb2(cliapp.Application):

    def setup(self):
        self.step_runners = vmdb.StepRunnerList()

    def process_args(self, args):
        spec = self.load_spec_file(args[0])

        steps = spec['steps']
        steps_taken, core_meltdown = self.run_steps(steps)
        self.run_teardowns(steps_taken)
        
        if core_meltdown:
            logging.error('An error step was used, exiting with error')
            sys.exit(1)

    def load_spec_file(self, filename):
        sys.stdout.write('Load spec file {}\n'.format(filename))
        logging.info('Load spec file %s', filename)
        with open(filename) as f:
            return yaml.safe_load(f)

    def run_steps(self, steps):
        core_meltdown = False
        steps_taken = []

        try:
            for step in steps:
                steps_taken.append(step)
                runner = self.step_runners.find(step)
                runner.run(step)
        except Exception as e:
            logging.error('ERROR: %s', str(e))
            sys.stderr.write('ERROR: {}\n'.format(str(e)))
            core_meltdown = True

        return steps_taken, core_meltdown

    def run_teardowns(self, steps_taken):
        for step in reversed(steps_taken):
            if 'teardown' in step:
                runner = self.step_runners.find(step)
                runner.teardown(step)
