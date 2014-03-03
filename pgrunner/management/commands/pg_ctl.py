from django.core.management.base import BaseCommand
import subprocess
from pgrunner import bin_path

from pgrunner.commands import get_port, CURRENT

class Command(BaseCommand):
    help = 'Run pg_ctl with correct data dir'

    def run_from_argv(self, argv):
        pg_ctl = bin_path('pg_ctl')
        if '--help' in argv:
            cmd = [pg_ctl, '--help']
        else:
            cmd = [pg_ctl, '-D', CURRENT]
            cmd.extend(argv[2:])
        print(' '.join(cmd))
        subprocess.call(cmd)

