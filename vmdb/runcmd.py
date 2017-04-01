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


def runcmd(argv, *argvs, **kwargs):
    kwargs['stdout_callback'] = _log_stdout
    kwargs['stderr_callback'] = _log_stderr
    return cliapp.runcmd(argv, *argvs, **kwargs)


def _log_stdout(data):
    logging.debug('STDOUT: %r', data)
    sys.stdout.write(data)
    if not data.endswith('\n'):
        sys.stdout.write('\n')
    return data


def _log_stderr(data):
    logging.debug('STDERR: %r', data)
    sys.stderr.write(data)
    if not data.endswith('\n'):
        sys.stderr.write('\n')
    return data
