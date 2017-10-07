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


import io
import os
import tempfile
import unittest

import yaml

import vmdb


class SpecTests(unittest.TestCase):

    spec_yaml = '''
    steps:
      - step: foo
      - step: bar
    '''

    def test_loads_spec(self):
        filename = write_temp_file(bytes(self.spec_yaml, 'ascii'))
        spec = vmdb.Spec()
        spec.load_file(filename)
        self.assertEqual(spec.as_dict(), as_dict(self.spec_yaml))


def write_temp_file(data):
    fd, filename = tempfile.mkstemp()
    os.write(fd, data)
    os.close(fd)
    return filename


def as_dict(yaml_text):
    with io.StringIO(yaml_text) as f:
        return yaml.safe_load(f)
