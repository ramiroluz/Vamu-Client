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
import re

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

        self.file_options = ['input', 'output', 'bibtex', 'size']

    def __setitem__(self, key, value):
        if key not in self.file_options:
            valid_values = self.valid_options.get(key)
            if not valid_values:
                raise InvalidOptionError
            if value not in valid_values:
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

        And some options to deal with files:
        -i --input          Input file with URLs to short.
        -o --output         Output file to store shorted URLs
                            DANGER (file will be overrided).
                            
        -b --bibtex         Bibtex file to convert references.
        -s --size           Minimum URL length to convert. (default:42).           
        '''
        self.api_template = 'http://va.mu/api/create?url={0}'

        #TODO handle args
        self.options = Options(kwargs)
        if 'size' not in self.options:
            self.options['size'] = 42

        self.shorted = []
        self.handle_options()

    def set_url(self, url):
        self.handle_options()
        self.resource = self.api.format(urllib2.quote(url))
        return self.resource

    def run(self):
        out_file_name = self.options.get('output')
        in_file_name = self.options.get('input')
        bib_file_name = self.options.get('bibtex')
        if bib_file_name:
            result = self.short_bibtex_file(bib_file_name, out_file_name)
        else:
            if in_file_name:
                self.short_from_file(in_file_name)
            else:
                self.short_list([self.options.get('url')])

            if out_file_name:
                result = self.write(out_file_name)
            else:
                result = '\n'.join(self.shorted)
                
        return result

    def short_bibtex_file(self, bib_file_name, out_file_name = None):
        try:
            read_file = open(bib_file_name)
            url_pattern = re.compile('''[\{]http://[^+]*?[\}]''')
            content = read_file.read()
            read_file.close()
            urls = url_pattern.findall(content)
            replaces = [x for x in urls if len(x) > self.options.get('size')]
            
            for bib_url in replaces:
                url = bib_url.replace('\\','')
                url = url.replace('},\n','')
                url = url.replace('}\n','')
                content = content.replace(url, self.short_url(url))
                print '.',
                
            if out_file_name is None:
                out_file_name = bib_file_name
            write_file = open(out_file_name,'w')
            write_file.write(content)
            write_file.close()
            result = 'Bibtex file shorted: {0}'.format(bib_file_name)
        except:
            result = 'Couldn\'t short from bibtex file: {0}'
            result = result.format(bib_file_name)
        return result
            
    def short_from_file(self, in_file_name):
        try:
            in_file = open(out_file_name, 'w')
            rows = in_file.readlines()
            self.short_list(rows)
            result = 'File shorted: {0}'.format(in_file_name)
        except:
            result = 'Couldn\'t short from file: {0}'.format(in_file_name)
        return result
            
            
    def write(self, out_file_name):
        try:
            out_file = open(out_file_name, 'w')
            for row in self.sorted:
                out_file.write('{0[0]} - {0[1]}\n'.format(row))
            out_file.close()
            result = 'Output file generated: {0}'.format(out_file_name)
        except:
            result = 'Couldn\'t generate file: {0}'.format(out_file_name)
        return result

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
        self.shorted = []
        for url in urls:
            self.shorted.append((url, self.short_url(url)))
        return self.shorted

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
    -i --input          Input file with URLs to short.
    -o --output         Output file to store shorted URLs.
    -b --bibtex         Bibtex file to convert references.
    -s --size           Minimum URL length to convert. (default:42).

    -u --url            Required URL

    More information: http://va.mu/api/doc
    '''.format(sys.argv[0]))

    
def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hc:e:C:t:u:i:o:b:s:", 
                                  ["help", "canonical=",
                                   "exclusive=", "confirmation=",
                                   "type=", "url=", "input=",
                                   "output=", "bibtex=", "size="])
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
        elif o in ("-i", "--input"):
            options['input'] = a
        elif o in ("-o", "--output"):
            options['output'] = a
        elif o in ("-b", "--bibtex"):
            options['bibtex'] = a
        elif o in ("-s", "--size"):
            options['size'] = a
        else:
            assert False, "unhandled option"

    if url or options.get('input') or options.get('bibtex'):
        vamu = VamuClient()
        vamu.options = options
        vamu.set_url(url)
        print( vamu.run() )
    else:
        print('URL is required.')
        usage()
        sys.exit(2)


if __name__ == '__main__':
    main()
