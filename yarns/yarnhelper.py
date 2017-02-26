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


import email
import imaplib
import os
import subprocess
import urlparse

import requests
import yaml


variables_filename = os.environ.get('VARIABLES', 'vars.yaml')


class YarnHelper(object):

    def __init__(self):
        self._env = dict(os.environ)
        self._next_match = 1
        self._variables = None  # None means not loaded, otherwise dict

    def set_environment(self, env):
        self._env = dict(env)

    def get_next_match(self):
        name = 'MATCH_{}'.format(self._next_match)
        if name not in self._env:
            raise Error('no next match')
        self._next_match += 1
        return self._env[name]

    def get_variable(self, name):
        if self._variables is None:
            self._variables = self._load_variables()
        if name not in self._variables:
            raise Error('no variable {}'.format(name))
        return self._variables[name]

    def _load_variables(self):
        if os.path.exists(variables_filename):
            with open(variables_filename, 'r') as f:
                return yaml.safe_load(f)
        return {}

    def set_variable(self, name, value):
        if self._variables is None:
            self._variables = {}
        self._variables[name] = value
        self._save_variables(self._variables)

    def _save_variables(self, variables):
        with open(variables_filename, 'w') as f:
            yaml.safe_dump(variables, f)

    def construct_aliased_http_request(
            self, address, method, url, data=None, headers=None):

        if headers is None:
            headers = {}

        parts = list(urlparse.urlparse(url))
        headers['Host'] = parts[1]
        parts[1] = address
        aliased_url = urlparse.urlunparse(parts)

        r = requests.Request(method, aliased_url, data=data, headers=headers)
        return r.prepare()

    def http_get(self, address, url):  # pragma: no cover
        r = self.construct_aliased_http_request(address, 'GET', url)
        s = requests.Session()
        resp = s.send(r)
        return resp.status_code, resp.content

    def assertEqual(self, a, b):
        if a != b:
            raise Error('assertion {!r} == {!r} failed'.format(a, b))

    def assertNotEqual(self, a, b):
        if a == b:
            raise Error('assertion {!r} != {!r} failed'.format(a, b))

    def assertGreaterThan(self, a, b):
        if a <= b:
            raise Error('assertion {!r} > {!r} failed'.format(a, b))

    def get_password_with_pass(self, pass_home, pass_name):  # pragma: no cover
        p = subprocess.Popen(
            ['env', 'HOME={}'.format(pass_home), 'pass', 'show', pass_name],
            stdout=subprocess.PIPE)
        stdout, stderr = p.communicate()
        password = stdout.rstrip()
        return password

    def iterate_mails_in_imap_mailbox(
            self, address, user, password, callback, exp):  # pragma: no cover
        m = imaplib.IMAP4_SSL(address)
        m.login(user, password)
        m.select('INBOX', False)
        typ, data = m.search(None, 'ALL')
        for num in data[0].split():
            typ, data = m.fetch(num, '(RFC822)')
            typ, text = data[0]
            msg = email.message_from_string(text)
            callback(m, num, msg)
        if exp:
            m.expunge()
        m.close()
        m.logout()


class Error(Exception):

    pass
