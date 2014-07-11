from __future__ import (absolute_import, division, print_function, unicode_literals)

from django.core.management.base import BaseCommand, CommandError
import subprocess
import os
from os.path import join, exists
import time

from pgrunner.commands import ROOT, activate_clone, \
    ensure_stopped, ensure_started


class Command(BaseCommand):
    help = 'Activate a snapshot'
    args = '<snapshot-name>'

    def list_snapshots(self):
        print("Available snapshots:")
        for name in os.listdir(ROOT):
            if name == 'current' or name.startswith('.'):
                continue
            if exists(join(ROOT, name, 'postgresql.conf')):
                print('-', name)

    def handle(self, *args, **options):
        if not args:
            self.list_snapshots()
            return

        snapshot = args[0]
        if snapshot == 'current':
            raise CommandError("Invalid snapshot name")

        if not exists(join(ROOT, snapshot)):
            self.list_snapshots()
            raise CommandError("Snapshot not found: {0}".format(snapshot))

        running = ensure_stopped(verbose=True)

        activate_clone(snapshot)

        if running:
            ensure_started(verbose=True)
            print("Server restarted in background.")

        print()
        print("Snapshot activated.")

