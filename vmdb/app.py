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
import jinja2

import yaml

import vmdb


class Vmdb2(cliapp.Application):

    def add_settings(self):
        self.settings.string(
            ['image'],
            'create image file FILE',
            metavar='FILE')

    def setup(self):
        self.step_runners = vmdb.StepRunnerList()

    def process_args(self, args):
        spec = self.load_spec_file(args[0])

        steps = spec['steps']
        state = vmdb.State()
        steps_taken, core_meltdown = self.run_steps(steps, state)
        self.run_teardowns(steps_taken, state)

        if core_meltdown:
            logging.error('An error step was used, exiting with error')
            sys.exit(1)

    def load_spec_file(self, filename):
        sys.stdout.write('Load spec file {}\n'.format(filename))
        logging.info('Load spec file %s', filename)
        with open(filename) as f:
            return yaml.safe_load(f)

    def run_steps(self, steps, state):
        core_meltdown = False
        steps_taken = []

        try:
            for step in steps:
                steps_taken.append(step)
                expanded_step = self.expand_step_spec(step)
                runner = self.step_runners.find(step)
                runner.run(expanded_step, self.settings, state)
        except Exception as e:
            logging.error('ERROR: %s', str(e))
            sys.stderr.write('ERROR: {}\n'.format(str(e)))
            core_meltdown = True

        return steps_taken, core_meltdown

    def run_teardowns(self, steps_taken, state):
        for step in reversed(steps_taken):
            expanded_step = self.expand_step_spec(step)
            runner = self.step_runners.find(step)
            runner.teardown(expanded_step, self.settings, state)

    def expand_step_spec(self, step):
        expanded = {}
        for key in step:
            expanded[key] = self.expand_jinja2(step[key])
        return expanded

    def expand_jinja2(self, value):
        template = jinja2.Template(value)
        vars = self.create_template_vars()
        return template.render(**vars)

    def create_template_vars(self):
        vars = dict()
        for key in self.settings:
            vars[key] = self.settings[key]
        return vars
