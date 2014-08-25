from __future__ import absolute_import, division, print_function, unicode_literals

import os
import subprocess
import random
from os.path import join
import time
import datetime
import shutil

from django.core.management.base import BaseCommand, CommandError

from pgrunner import bin_path
from pgrunner.commands import ROOT, DEFAULT, activate_clone, \
    get_port, ensure_stopped, ensure_started, \
    current_clone


class Command(BaseCommand):
    help = 'Create a new blank database'

    def handle(self, *args, **options):
        if not os.path.isdir(ROOT):
            raise CommandError(
                'Root does not exist, maybe you meant pg_init? {0}'.format(ROOT))

        previous = current_clone()

        # Name for clone
        name = '{:%Y%m%d-%H%M%S}'.format(datetime.datetime.now())
        target = join(ROOT, name)

        cmd = [bin_path('initdb'), target]
        print(' '.join(cmd))
        if subprocess.call(cmd) > 0:
            raise CommandError('Error creating database in {0}'.format(target))

        for fname in ['pg_hba.conf', 'postgresql.conf']:
            src = os.path.join(DEFAULT, fname)
            dst = os.path.join(ROOT, name, fname)
            shutil.copyfile(src, dst)

        print("Stopping server")
        ensure_stopped()

        print("New database in {0}".format(target))
        activate_clone(name)

        print("Starting server to create database 'django'")
        ensure_started()

        print("Pausing 3s so that the database can start up")
        time.sleep(3)

        print("Creating database 'django'")
        cmd = [bin_path('createdb'), '-p', str(get_port()),
               '-h', '127.0.0.1', 'django']
        print(' '.join(cmd))
        if subprocess.call(cmd) > 0:
            raise CommandError('Error creating database')

        print("Blank database {} created and activated".format(name))
        print()
        print("To revert to your previous clone:")
        print()
        print("    ./manage.py pg_activate {}".format(previous))