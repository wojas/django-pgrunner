from django.core.management.base import BaseCommand
import subprocess
from pgrunner import bin_path

from pgrunner.commands import get_port, CURRENT

class Command(BaseCommand):
    help = 'Run pg_ctl with correct data dir'

    def handle(self, *args, **options):
        cmd = [bin_path('pg_ctl'), '-D', CURRENT]
        cmd.extend(args)
        print(' '.join(cmd))
        subprocess.call(cmd)

