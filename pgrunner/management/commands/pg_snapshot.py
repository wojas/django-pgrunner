from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
import subprocess
from os.path import join, exists

from pgrunner.commands import ROOT, CURRENT, \
    ensure_stopped, ensure_started, activate_clone


class Command(BaseCommand):
    help = 'Create a named snapshot of the database'
    args = '<snapshot-name>'
    option_list = BaseCommand.option_list + (
        make_option('--activate',
            action='store_true',
            dest='activate',
            default=False,
            help='Immediately activate the snapshot after creating it'),
    )

    def handle(self, *args, **options):
        if not args:
            raise CommandError("No snapshot name specified")
        snapshot = args[0]
        snapshot_path = join(ROOT, snapshot)
        if exists(snapshot_path):
            raise CommandError("Snapshot already exists: {0}".format(snapshot_path))

        running = ensure_stopped(verbose=True)

        # rsync must be in the system PATH
        cmd = ['rsync', '-aP', '--progress', CURRENT + '/.', snapshot_path]
        print(' '.join(cmd))
        if subprocess.call(cmd) > 0:
            raise CommandError("rsync failed")

        if options['activate']:
            print('Activating the snapshot.')
            activate_clone(snapshot)

        if running:
            ensure_started(verbose=True)
            print("Server restarted in background.")

        print()
        print("Snapshot done.")

        if not options['activate']:
            print()
            print("To activate:")
            print()
            print("    ./manage.py pg_activate", snapshot)


