from __future__ import absolute_import, division, print_function, unicode_literals

from django.core.management.base import BaseCommand

from pgrunner.commands import is_running


class Command(BaseCommand):
    help = 'Manually check the output of our is_running() function'

    def run_from_argv(self, argv):
        print(is_running())

