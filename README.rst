unofficial mirror of pygenie, a tool for measuring cyclomatic complexity
http://www.traceback.org/2008/03/31/measuring-cyclomatic-complexity-of-python-code/

To measure complexity of your django applications:

1. Add `djangopygenie` to your `INSTALLED_APPS`
2. List any applications you want not to be measured in `PYGENIE_SKIP_APPS` in `settings.py`. It's default value is:
    (
        'djangopygenie',
        '^django\.contrib\.',
    )
3. Execute `python manage.py complexity [--verbose]`