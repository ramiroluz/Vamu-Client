#!/usr/bin/env python
#
# main.py
# Copyright (C) Ramiro Batista da Luz 2011 <ramiroluz@gmail.com>
# 
# vamu-client is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# vamu-client is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

import urllib2
import getopt
import sys

class InvalidOptionError(Exception):
    pass

class InvalidValueError(Exception):
    pass

class Options(dict):
    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)
    
        self.valid_options = {'canonical': ['0', '1'],
                              'exclusive': ['0', '1'],
                              'confirmation': ['0', '1'],
                              'type': ['plain', 'json', 'xml']}
        
    def __setitem__(self, key, value):
        v = self.valid_options.get(key)

        if not v:
            raise InvalidOptionError
        
        if value not in v:
            raise InvalidValueError
        
        dict.__setitem__(self, key, value)

    def update(self, *args, **kwargs):
        for k, v in dict(*args, **kwargs).iteritems():
            self[k] = v
            
class VamuClient():
    def __init__(self, *args, **kwargs):
        '''Accept the following options, from http://va.mu/api/doc

        canonical (optional): Return the canonical URL or an short URL (default: 0).
        exclusive (optional): Define a new exclusive URL (default: 0).
        confirmation (optional): Define if it should show a confirmation page.(default: 0).
        type (optional): Return type: plain, json, xml (default: plain).
        '''
        self.api_template = 'http://va.mu/api/create?url={0}'

        #TODO handle args
        self.options = Options(kwargs)
        self.handle_options()

    def set_url(self, url):
        self.handle_options()
        self.resource = self.api.format(urllib2.quote(url))
        return self.resource

    def get_short_url(self):
        return self.short_url()
    
    def handle_options(self):
        optional_args = []
        for key, value in self.options.iteritems():
            optional_args.append('{0}={1}'.format(key,value))
        if optional_args:
            self.api = '{0}&{1}'.format(self.api_template,
                                        '&'.join(optional_args))
        else:
            self.api = self.api_template
            
    def short_list(self, urls):
        shorted = []
        for url in urls:
            shorted.append((url, self.short_url(url)))
        return shorted

    def short_url(self, url=None):
        if url:
            self.set_url(url)
        shorted_url = urllib2.urlopen(self.resource).read()
        return shorted_url

def usage():
    print('''Usage:
    {0} [OPTIONS] -u URL
or
    {0} [OPTIONS] -url URL

    Where options are:
    -h --help           Print this message
    -c --canonical      Return the canonical URL or an short URL (default: 0).
    -e --exclusive      Define a new exclusive URL (default: 0).
    -C --confirmation   Define if it should show a confirmation page.
                        (default: 0).
    -t --type           Return type: plain, json, xml (default: plain).

    -u --url            Required URL

    More information: http://va.mu/api/doc
    ''')

    
def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hc:e:C:t:u:", 
                                  ["help", "canonical=",
                                   "exclusive=","confirmation=",
                                   "type=","url="])
    except getopt.GetoptError, err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    options = {}
    url = ''
    for o, a in opts:
        if o in ["-c", "--canonical"]:
            options['canonical'] = a
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-e", "--exclusive"):
            options['exclusive'] = a
        elif o in ("-C", "--confirmation"):
            options['confirmation'] = a
        elif o in ("-t", "--type"):
            options['type'] = a
        elif o in ("-u", "--url"):
            url = a
        else:
            assert False, "unhandled option"

    if url:
        vamu = VamuClient()
        vamu.options = options
        vamu.set_url(url)
        print( vamu.get_short_url() )
    else:
        print('URL is required.')
        usage()
        sys.exit(2)


if __name__ == '__main__':
    main()
