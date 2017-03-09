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
