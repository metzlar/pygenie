#!/usr/bin/env python

import os
import sys
import traceback
from glob import glob
from optparse import OptionParser

import cc


COMMANDS = ['all', 'complexity', ]
USAGE = 'usage: pygenie command [directories|files|packages]'


class CommandParser(object):

    def __init__ (self, optparser, commands):
        self.commands = commands or []
        self.optparser = optparser

    def parse_args(self, args=None, values=None):
        args = args or sys.argv[1:]
        if len(args) < 1:
            self.optparser.error('please provide a valid command')

        command = args[0]
        if command not in self.commands:
            self.optparser.error("'%s' is not a valid command" % command)

        options, values = self.optparser.parse_args(args[1:], values)
        return command, options, values


def find_module(fqn):
    join = os.path.join
    exists = os.path.exists
    partial_path = fqn.replace('.', os.path.sep)
    for p in sys.path:
        path = join(p, partial_path, '__init__.py')
        if exists(path):
            return path
        path = join(p, partial_path + '.py')
        if exists(path):
            return path
    raise Exception('invalid module')


def find_dir(fqn):
    items = []
    for f in glob(os.path.join(fqn, '*')):
        if os.path.isfile(f) and f.endswith('.py'):
            items.append(os.path.abspath(f))
        elif os.path.isdir(f):
            items += find_dir(os.path.abspath(f))
    return items


def main():
    from optparse import OptionParser

    parser = OptionParser(usage='./cc.py command [options] *.py')
    parser.add_option('-v', '--verbose',
            dest='verbose', action='store_true', default=False,
            help='print detailed statistics to stdout')
    parser = CommandParser(parser, COMMANDS)
    command, options, args = parser.parse_args()

    items = []
    for arg in args:
        if os.path.isdir(arg):
            items += find_dir(arg)
            #for f in glob(os.path.join(arg, '*.py')):
            #    if os.path.isfile(f):
            #        items.add(os.path.abspath(f))
        elif os.path.isfile(arg):
            items.append(os.path.abspath(arg))
        else:
            # this should be a package'
            items.append(find_module(arg))
            
    items = set(items)

    for item in items:
        code = open(item).read()
        if command in ('all', 'complexity'):
            try:
                stats = cc.measure_complexity(code, item)
                pp = cc.PrettyPrinter(sys.stdout, verbose=options.verbose)
                pp.pprint(item, stats)
            except Exception, e:
                sys.stdout.write('Error %s while measuring %s' % (str(e), item))
                traceback.print_exc()
                continue

if __name__ == '__main__':
    main()
