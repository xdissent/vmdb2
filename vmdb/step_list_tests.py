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


import unittest

import vmdb


class StepRunnerListTests(unittest.TestCase):

    def test_is_empty_initially(self):
        steps = vmdb.StepRunnerList()
        self.assertEqual(len(steps), 0)

    def test_adds_a_runner(self):
        steps = vmdb.StepRunnerList()
        runner = DummyStepRunner()
        steps.add(runner)
        self.assertEqual(len(steps), 1)

    def test_finds_correct_runner(self):
        steps = vmdb.StepRunnerList()
        runner = DummyStepRunner()
        steps.add(runner)
        found = steps.find({'foo': None, 'bar': None})
        self.assertEqual(runner, found)

    def test_raises_error_if_runner_not_found(self):
        steps = vmdb.StepRunnerList()
        runner = DummyStepRunner()
        steps.add(runner)
        with self.assertRaises(vmdb.NoMatchingRunner):
            steps.find({'foo': None})


class DummyStepRunner(vmdb.StepRunnerInterface):

    def run(self, *args):
        pass

    def get_required_keys(self):
        return ['foo', 'bar']
