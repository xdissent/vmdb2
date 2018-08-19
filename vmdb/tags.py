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


# Unmount a directory, including any mount points under that
# directory. If /mnt/foo is given, and /mnt/foo/bar is also mounted,
# unmount /mnt/foo/bar first, and /mnt/foo then. Look for sub-mounts
# in /proc/mounts.


import vmdb


class Image:

    def __init__(self):
        self._tags = {}

    def get_tags(self):
        return list(self._tags.keys())

    def has_tag(self, tag):
        return tag in self._tags

    def get_dev(self, tag):
        item = self._tags.get(tag)
        if item is None:
            raise UnknownTag(tag)
        return item['dev']

    def get_mount_point(self, tag):
        item = self._tags.get(tag)
        if item is None:
            raise UnknownTag(tag)
        return item['mount_point']

    def add_partition(self, tag, dev):
        if tag in self._tags:
            raise TagInUse(tag)
        self._new(tag, dev, None)

    def add_mount_point(self, tag, mount_point):
        item = self._tags.get(tag)
        if item is None:
            raise UnknownTag(tag)
        if item['mount_point'] is not None:
            raise AlreadyMounted(tag)
        item['mount_point'] = mount_point

    def _new(self, tag, dev, mount_point):
        self._tags[tag] = {
            'dev': dev,
            'mount_point': mount_point,
        }


class TagInUse(Exception):

    def __init__(self, tag):
        super().__init__('Tag already used: {}'.format(tag))


class UnknownTag(Exception):

    def __init__(self, tag):
        super().__init__('Unknown tag: {}'.format(tag))


class AlreadyMounted(Exception):

    def __init__(self, tag):
        super().__init__('Already mounted tag: {}'.format(tag))
