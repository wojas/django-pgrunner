from django.core.management.base import BaseCommand, CommandError
import subprocess
from pgrunner import bin_path

from pgrunner.commands import get_port

class Command(BaseCommand):
    help = 'Run psql with correct database'

    def run_from_argv(self, argv):
        port = get_port()
        cmd = [bin_path('psql'), '-p', str(port), '-h', '127.0.0.1', 'django']
        cmd.extend(argv[2:])
        print(' '.join(cmd))
        subprocess.call(cmd)
