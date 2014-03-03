import os
import subprocess
import random
from os.path import join
import time

from django.core.management.base import BaseCommand, CommandError

from pgrunner import DEFAULT_NAME, bin_path
from pgrunner.commands import ROOT, DEFAULT, activate_clone, \
    set_port, get_port, CURRENT, HELP

SETTINGS = """
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'django',
        'USER': '',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': $port$
    }
}
"""

PORT_MIN = 15000
PORT_MAX = 16000

class Command(BaseCommand):
    help = 'Initializes a new local PostgreSQL database'

    def handle(self, *args, **options):
        if os.path.isdir(ROOT):
            raise CommandError('Directory already exists: {0}'.format(ROOT))

        print("Creating new PostgreSQL root for development in {0}".format(ROOT))
        os.mkdir(ROOT)

        cmd = [bin_path('initdb'), DEFAULT]
        print(' '.join(cmd))
        if subprocess.call(cmd) > 0:
            raise CommandError('Error creating database in {0}'.format(DEFAULT))
        activate_clone('default')

        print("New database in {0}".format(DEFAULT))

        # TODO: create option to pick a specific one
        port = random.randint(PORT_MIN, PORT_MAX)
        set_port(port)
        if get_port() != port:
            raise CommandError('Setting port failed')
        print("Port set to {0} (can be changed in {1})".format(
            port, join(DEFAULT, 'postgresql.conf')))

        # TODO: number of requested standby connections exceeds
        #       max_wal_senders (currently 0)
        print("Enabling replication permissions in pg_hba.conf")
        pg_hba_path = join(CURRENT, 'pg_hba.conf')
        with open(pg_hba_path, 'r') as f:
            pg_hba = f.read().split('\n')
        with open(pg_hba_path, 'w') as f:
            for line in pg_hba:
                if len(line) > 2 and line[0] == '#' and line[1] != ' ':
                    # Strip comment character
                    line = line[1:]
                f.write(line + '\n')

        print("Starting server to create database 'django'")
        cmd = [bin_path('pg_ctl'), '-D', CURRENT, 'start']
        print(' '.join(cmd))
        if subprocess.call(cmd) > 0:
            raise CommandError('Error starting database')

        print("Pausing 3s so that the database can start up")
        time.sleep(3)

        print("Creating database 'django'")
        cmd = [bin_path('createdb'), '-p', str(port), '-h', '127.0.0.1', 'django']
        print(' '.join(cmd))
        if subprocess.call(cmd) > 0:
            raise CommandError('Error creating database')

        print("Stopping server")
        cmd = [bin_path('pg_ctl'), '-D', CURRENT, 'stop']
        print(' '.join(cmd))
        if subprocess.call(cmd) > 0:
            raise CommandError('Error stopping database')

        print()
        print("Example configuration for settings.py:")
        settings = SETTINGS.replace('$port$', str(port))
        print(settings)
        with open(join(ROOT, 'settings.py'), 'w') as f:
            f.write(settings)

        #print()
        #print("These settings have been written to postgresdb/settings.py")
        #print("At the end of your settings.py or local settings file, add:")
        #print()
        #print("from {0}.settings import *".format(DEFAULT_NAME))
        print()
        print("Simply add this at the end of your settings file to")
        print("automatically set the right database settings and start the ")
        print("database if needed:")
        print()
        print('import pgrunner')
        print('pgrunner.settings(locals())')
        print()
        print(HELP)

