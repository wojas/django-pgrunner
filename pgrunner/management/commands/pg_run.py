from __future__ import absolute_import, division, print_function, unicode_literals

from django.core.management.base import BaseCommand, CommandError
import subprocess
from pgrunner import bin_path

from pgrunner.commands import get_port, CURRENT

class Command(BaseCommand):
    help = 'Start PostgreSQL in foreground'

    def handle(self, *args, **options):
        print("Starting server on port", get_port())
        cmd = [bin_path('postgres'), '-D', CURRENT]
        print(' '.join(cmd))
        subprocess.call(cmd)
