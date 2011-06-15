# vamu_client_test.py
#
# Copyright (C) 2011 - Ramiro Batista da Luz
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import unittest
from vamu_client import VamuClient, InvalidValueError, InvalidOptionError

class VamuClientTest(unittest.TestCase):
    def setUp(self):
        self.vamu = VamuClient()

    def test_set_default_url(self):
        self.vamu.set_url('http://www.google.com')
        result = 'http://va.mu/api/create?url=http%3A//www.google.com' 
        self.assertEqual(self.vamu.resource, result)

    def test_set_url_with_canonical(self):
        self.vamu.options['canonical'] = '1'
        self.vamu.set_url('http://www.google.com')
        result = 'http://va.mu/api/create?url=http%3A//www.google.com&canonical=1' 
        self.assertEqual(self.vamu.resource, result)

    def test_set_url_with_exclusive(self):
        self.vamu.options['exclusive'] = '1'
        self.vamu.set_url('http://www.google.com')
        result = 'http://va.mu/api/create?url=http%3A//www.google.com&exclusive=1' 
        self.assertEqual(self.vamu.resource, result)

    def test_set_url_with_confirmation(self):
        self.vamu.options['confirmation'] = '1'
        self.vamu.set_url('http://www.google.com')
        result = 'http://va.mu/api/create?url=http%3A//www.google.com&confirmation=1' 
        self.assertEqual(self.vamu.resource, result)

    def test_set_url_with_type(self):
        self.vamu.options['type'] = 'json'
        self.vamu.set_url('http://www.google.com')
        result = 'http://va.mu/api/create?url=http%3A//www.google.com&type=json' 
        self.assertEqual(self.vamu.resource, result)

    def test_handle_default_options(self):
        self.vamu.handle_options()
        self.assertEqual(self.vamu.options, {})

    def test_set_valid_canonical(self):
        self.vamu.options['canonical'] = '1'
        self.assertEqual(self.vamu.options.get('canonical'), '1')

    def test_set_invalid_canonical(self):
        self.assertRaises(InvalidValueError, 
                          self.vamu.options.update,
                          canonical='10')

    def test_set_valid_exclusive(self):
        self.vamu.options['exclusive'] = '1'
        self.assertEqual(self.vamu.options, {'exclusive':'1'})

    def test_set_invalid_exclusive(self):
        self.assertRaises(InvalidValueError, 
                          self.vamu.options.update,
                          exclusive=1)

    def test_set_valid_confirmation(self):
        self.vamu.options['confirmation'] = '1'
        self.assertEqual(self.vamu.options, {'confirmation':'1'})

    def test_set_invalid_confirmation(self):
        self.assertRaises(InvalidValueError, 
                          self.vamu.options.update,
                          confirmation=True)

    def test_set_valid_type(self):
        self.vamu.options['type'] = 'xml'
        self.assertEqual(self.vamu.options, {'type':'xml'})

    def test_set_invalid_type(self):
        self.assertRaises(InvalidValueError, 
                          self.vamu.options.update,
                          type='pdf')

    def test_set_invalid_option(self):
        self.assertRaises(InvalidOptionError, 
                          self.vamu.options.update,
                          noname='1')
        
if __name__ == '__main__':
    unittest.main()