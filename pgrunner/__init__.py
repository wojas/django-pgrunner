import os
import sys
from django.core.exceptions import ImproperlyConfigured

DEFAULT_NAME = 'pgrunnerdb'
DEFAULT_ROOT = os.path.join(os.getcwd(), DEFAULT_NAME)
ROOT = DEFAULT_ROOT
BIN = None

def bin_path(name):
    """Convert a binary name to a full path if needed

    :param name: name of binary
    :type name: str
    :return: full path to binary, or just the name if in PATH
    :rtype: str
    """
    if BIN:
        return os.path.join(BIN, name)
    else:
        return name


def settings(settings_locals, start=True):
    """Register settings for PostgreSQL dev database

    This will set `DATABASES['default']` to the right values for the development
    environment, and start the database server if needed.

    Usage in `settings.py`::

        # Make sure to do this after DATABASES and any settings for this module
        import pgrunner
        pgrunner.settings(locals())

    :param settings_locals: locals() in settings.py
    :type settings_locals: dict
    """
    global ROOT, BIN
    ROOT = settings_locals.get('PGRUNNER_ROOT', None)
    if not ROOT:
        ROOT = DEFAULT_ROOT
    BIN = settings_locals.get('PGRUNNER_BIN', None)
    if BIN and not (os.path.isdir(BIN) and os.path.exists(bin_path('initdb'))):
        raise ImproperlyConfigured(
            "PGRUNNER_BIN setting incorrect: "
            "no folder or initdb not found in {0}".format(BIN))

    db_exists = os.path.exists(ROOT)

    from pgrunner.commands import get_port, ensure_started

    if not db_exists:
        print("PostgreSQL dev root does not exist:", ROOT)
        print("Not changing any settings.")
        print("Please run `./manage.py pg_init` first!")

    if db_exists:
        if not 'DATABASES' in settings_locals:
            settings_locals['DATABASES'] = {}

        settings_locals['DATABASES']['default'] = {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'django',
            'USER': '',
            'PASSWORD': '',
            'HOST': '127.0.0.1',
            'PORT': get_port()
        }

    running_own_command = False
    if len(sys.argv) > 1 and sys.argv[0].endswith('manage.py') \
            and sys.argv[1].startswith('pg_'):
        running_own_command = True

    help = len(sys.argv) == 1 and sys.argv[0].endswith('manage.py')

    if db_exists and start and not running_own_command and not help:
        ensure_started(verbose=True)
