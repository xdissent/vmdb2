# Copyright 2018  Lars Wirzenius
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


class ImageTests(unittest.TestCase):

    def test_lists_not_tags_initally(self):
        image = vmdb.Image()
        self.assertEqual(image.get_tags(), [])

    def test_get_dev_raises_error_for_unknown_tag(self):
        image = vmdb.Image()
        with self.assertRaises(vmdb.UnknownTag):
            image.get_dev('does-not-exist')

    def test_get_mount_point_raises_error_for_unknown_tag(self):
        image = vmdb.Image()
        with self.assertRaises(vmdb.UnknownTag):
            image.get_mount_point('does-not-exist')

    def test_raises_error_for_reused_tag(self):
        image = vmdb.Image()
        image.add_partition('tag', 'dev')
        with self.assertRaises(vmdb.TagInUse):
            image.add_partition('tag', 'dev')

    def test_adds_partition(self):
        image = vmdb.Image()
        image.add_partition('first', '/dev/foo')
        self.assertEqual(image.get_tags(), ['first'])
        self.assertEqual(image.get_dev('first'), '/dev/foo')
        self.assertEqual(image.get_mount_point('first'), None)

    def test_adds_mount_point(self):
        image = vmdb.Image()
        image.add_partition('first', '/dev/foo')
        image.add_mount_point('first', '/mnt/foo')
        self.assertEqual(image.get_tags(), ['first'])
        self.assertEqual(image.get_dev('first'), '/dev/foo')
        self.assertEqual(image.get_mount_point('first'), '/mnt/foo')

    def test_add_mount_point_raises_error_for_unknown_tag(self):
        image = vmdb.Image()
        with self.assertRaises(vmdb.UnknownTag):
            image.add_mount_point('first', '/mnt/foo')

    def test_add_mount_point_raises_error_for_double_mount(self):
        image = vmdb.Image()
        image.add_partition('first', '/dev/foo')
        image.add_mount_point('first', '/mnt/foo')
        with self.assertRaises(vmdb.AlreadyMounted):
            image.add_mount_point('first', '/mnt/foo')
