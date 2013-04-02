from django.core.management.base import BaseCommand
import collections
import re
from pygenie import cc, find_dir, find_module
import os


class Command(BaseCommand):
    help = 'Measure complexity of your django applications'

    def handle(self, *args, **options):
        self.can_import_settings = True
        from django.conf import settings
        
        if hasattr(settings, 'PYGENIE_SKIP_APPS'):
            if isinstance(settings.PYGENIE_SKIP_APPS, collections.Iterable):
                skip = settings.PYGENIE_SKIP_APPS
        else:
            skip = [
                'djangopygenie',
                '^django\.contrib\.', 
            ]
        
        skip = [re.compile(s) for s in skip]
        
        modules = []
        
        for app in settings.INSTALLED_APPS:
            add = True
            for s in skip:
                if not s.match(app) is None:
                    add = False
            if add:
                modules.append(app)
                   
        items = [] 
        for module in modules:
            try:
                module = find_module(module)
                items += find_dir(os.path.dirname(module))
            except Exception, e:
                self.stderr.writeln('Error %s' % str(e))
                continue
        
        for item in items:
            code = open(item).read()
            try:
                stats = cc.measure_complexity(code, item)
                pp = cc.PrettyPrinter(self.stdout, verbose=False)
                pp.pprint(item, stats)
            except Exception, e:
                self.stderr.write('Error %s while measuring %s' % (str(e), item))
                traceback.print_exc(file=self.stderr)
                continue