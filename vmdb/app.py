import logging
import sys

import cliapp

import yaml

import vmdb


class Vmdb2(cliapp.Application):

    def setup(self):
        self.step_runners = vmdb.StepRunnerList()

    def process_args(self, args):
        filename = args[0]
        sys.stdout.write('Load spec file {}\n'.format(filename))
        logging.info('Load spec file %s', filename)
        spec = self.load_spec_file(filename)

        steps = spec['steps']
        steps_taken, core_meltdown = self.run_steps(steps)

        for step in reversed(steps_taken):
            if 'teardown' in step:
                runner = self.step_runners.find(step)
                runner.teardown(step)

        if core_meltdown:
            logging.error('An error step was used, exiting with error')
            sys.exit(1)

    def load_spec_file(self, filename):
        with open(filename) as f:
            return yaml.safe_load(f)

    def run_steps(self, steps):
        core_meltdown = False
        steps_taken = []

        for step in steps:
            steps_taken.append(step)
            runner = self.step_runners.find(step)
            core_meltdown = runner.run(step)
            if core_meltdown:
                break

        return steps_taken, core_meltdown
