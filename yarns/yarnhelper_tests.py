# Copyright 2016  Lars Wirzenius
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


import os
import unittest

import yarnhelper


class PersistentVariableTests(unittest.TestCase):

    def setUp(self):
        # We need this so that tearDown works
        pass

    def tearDown(self):
        if os.path.exists(yarnhelper.variables_filename):
            os.remove(yarnhelper.variables_filename)

    def test_raises_error_if_no_such_variable(self):
        h = yarnhelper.YarnHelper()
        with self.assertRaises(yarnhelper.Error):
            h.get_variable('FOO')
            print
            print 'variables:', h._variables

    def test_sets_variable_persistently(self):
        h = yarnhelper.YarnHelper()
        h.set_variable('FOO', 'bar')

        h2 = yarnhelper.YarnHelper()
        self.assertEqual(h2.get_variable('FOO'), 'bar')


class HttpTests(unittest.TestCase):

    def test_constructs_aliased_request(self):
        h = yarnhelper.YarnHelper()
        server = 'new.example.com'
        url = 'http://www.example.com/path'
        r = h.construct_aliased_http_request(server, 'GET', url)
        self.assertEqual(r.url, 'http://new.example.com/path')
        self.assertEqual(r.headers['Host'], 'www.example.com')


class AssertionTests(unittest.TestCase):

    def test_assertEqual_asserts_equals_correctly(self):
        h = yarnhelper.YarnHelper()
        self.assertEqual(h.assertEqual(0, 0), None)

    def test_assertEqual_raises_error_for_nonequal_values(self):
        h = yarnhelper.YarnHelper()
        with self.assertRaises(yarnhelper.Error):
            h.assertEqual(0, 1)

    def test_assertNotEqual_asserts_nonequal_correct(self):
        h = yarnhelper.YarnHelper()
        self.assertEqual(h.assertNotEqual(0, 1), None)

    def test_assertNotEqual_raises_error_for_equal_values(self):
        h = yarnhelper.YarnHelper()
        with self.assertRaises(yarnhelper.Error):
            h.assertNotEqual(0, 0)

    def test_assertGreaterThan_raises_error_for_equal_values(self):
        h = yarnhelper.YarnHelper()
        with self.assertRaises(yarnhelper.Error):
            h.assertGreaterThan(0, 0)

    def test_assertGreaterThan_raises_error_for_unordered_values(self):
        h = yarnhelper.YarnHelper()
        with self.assertRaises(yarnhelper.Error):
            h.assertGreaterThan(0, 1)
