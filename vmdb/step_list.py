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


import cliapp


class StepRunnerInterface(object):  # pragma: no cover

    def get_required_keys(self):
        raise NotImplementedError()

    def run(self, step_spec, settings):
        raise NotImplementedError()

    def teardown(self, step_spec, settings):
        # Default implementation does nop, so that sub-classes don't
        # need to have a nop teardown.
        pass


class StepRunnerList(object):

    def __init__(self):
        self._runners = []

    def __len__(self):
        return len(self._runners)

    def add(self, runner):
        self._runners.append(runner)

    def find(self, step_spec):
        actual = set(step_spec.keys())
        for runner in self._runners:
            required = set(runner.get_required_keys())
            if actual.intersection(required) == required:
                return runner
        raise NoMatchingRunner(actual)


class StepError(cliapp.AppException):

    pass


class NoMatchingRunner(cliapp.AppException):

    def __init__(self, keys):
        super(NoMatchingRunner, self).__init__(
            'No runner implements step with keys {}'.format(
            ', '.join(keys)))
