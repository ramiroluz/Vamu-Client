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
        self.bibtex_content = '''@Misc{CppUnit:01,
  Author         = {{Michael Feathers}},
  Title          = {Cpp{U}nit - the unit testing library},
  HowPublished   = {http://cppunit.sourceforge.net/doc/lastest/cppunit\_cookbook.html},
  Note           = {[Online; accessed 13-June-2011]},
  url            = {http://cppunit.sourceforge.net/doc/lastest/cppunit_cookbook.html}
}

@Misc{MichaelFeathers:03,
  Author         = {Feathers, Michael},
  Title          = {Source{F}orge.net: cppunit what is},
  HowPublished   = {http://sourceforge.net/apps/mediawiki/cppunit/index.php?title=Main\_Page\&oldid=50\#What\_is\_CppUnit.3F},
  Note           = {[Online; accessed 13-June-2011]},
  url            = {http://sourceforge.net/apps/mediawiki/cppunit/index.php?title=Main_Page&oldid=50#What_is_CppUnit.3F}
}'''
        self.bibtex_urls = ['http://cppunit.sourceforge.net/'
                            'doc/lastest/cppunit\\_cookbook.html',
                            'http://cppunit.sourceforge.net/'
                            'doc/lastest/cppunit_cookbook.html',
                            'http://sourceforge.net/apps/mediawiki/'
                            'cppunit/index.php?title=Main\_Page\&'
                            'oldid=50\#What\_is\_CppUnit.3F',
                            'http://sourceforge.net/apps/mediawiki/'
                            'cppunit/index.php?title=Main_Page&'
                            'oldid=50#What_is_CppUnit.3F']

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
        self.assertEqual(self.vamu.options, {'size':42})

    def test_set_valid_canonical(self):
        self.vamu.options['canonical'] = '1'
        self.assertEqual(self.vamu.options.get('canonical'), '1')

    def test_set_invalid_canonical(self):
        self.assertRaises(InvalidValueError, 
                          self.vamu.options.update,
                          canonical='10')

    def test_set_valid_exclusive(self):
        self.vamu.options['exclusive'] = '1'
        self.assertEqual(self.vamu.options.get('exclusive'), '1')

    def test_set_invalid_exclusive(self):
        self.assertRaises(InvalidValueError, 
                          self.vamu.options.update,
                          exclusive=1)

    def test_set_valid_confirmation(self):
        self.vamu.options['confirmation'] = '1'
        self.assertEqual(self.vamu.options.get('confirmation'), '1')

    def test_set_invalid_confirmation(self):
        self.assertRaises(InvalidValueError, 
                          self.vamu.options.update,
                          confirmation=True)

    def test_set_valid_type(self):
        self.vamu.options['type'] = 'xml'
        self.assertEqual(self.vamu.options.get('type'), 'xml')

    def test_findall_bibtex_urls(self):
        urls = self.vamu.findall_bibtex_urls(self.bibtex_content)
        self.assertEqual(urls, self.bibtex_urls)

    def test_handle_bibtex_urls(self):
        replaces = self.vamu.handle_bibtex_urls(self.bibtex_urls)
        self.assertEqual(replaces, [('http://cppunit.sourceforge.net/'
                                     'doc/lastest/cppunit\\_cookbook.html',
                                     'http://cppunit.sourceforge.net/'
                                     'doc/lastest/cppunit_cookbook.html'),
                                     ('http://cppunit.sourceforge.net/'
                                      'doc/lastest/cppunit_cookbook.html',
                                      'http://cppunit.sourceforge.net/'
                                      'doc/lastest/cppunit_cookbook.html'),
                                      ('http://sourceforge.net/apps/mediawiki/'
                                       'cppunit/index.php?title=Main\_Page\&'
                                       'oldid=50\#What\_is\_CppUnit.3F',
                                       'http://sourceforge.net/apps/mediawiki/'
                                       'cppunit/index.php?title=Main_Page&'
                                       'oldid=50#What_is_CppUnit.3F'),
                                      ('http://sourceforge.net/apps/mediawiki/'
                                       'cppunit/index.php?title=Main_Page&'
                                       'oldid=50#What_is_CppUnit.3F',
                                       'http://sourceforge.net/apps/mediawiki/'
                                       'cppunit/index.php?title=Main_Page&'
                                       'oldid=50#What_is_CppUnit.3F')])
                                
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