from __future__ import absolute_import, division, print_function, unicode_literals

from django.core.management.base import BaseCommand
import subprocess
from pgrunner import bin_path

from pgrunner.commands import get_port, ensure_stopped, ensure_started


class Command(BaseCommand):
    help = 'Run pg_restore with proper arguments'

    def run_from_argv(self, argv):
        running = None

        pg_cmd = bin_path('pg_restore')
        port = get_port()
        if '--help' in argv:
            cmd = [pg_cmd, '--help']
        else:
            cmd = [pg_cmd, '-p', str(port), '-h', '127.0.0.1', 'django', '-O']
            cmd.extend(argv[2:])
            running = ensure_started()
        print(' '.join(cmd))
        subprocess.call(cmd)

        if not running and running is not None:
            ensure_stopped()

