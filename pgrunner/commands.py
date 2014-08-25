from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys
from os.path import join
import re

import subprocess
import time

from pgrunner import ROOT

DEVNULL = open(os.devnull, 'wb')

# Default database (in the future we will put clones in the ROOT too)
DEFAULT = join(ROOT, 'default')

# Active database
CURRENT = join(ROOT, 'current')

HELP = """Useful commands
    ./manage.py pg_run           - Run PostgreSQL server in foreground
    ./manage.py pg_psql          - Start psql with right parameters
    ./manage.py pg_ctl start     - Start server in background
    ./manage.py pg_ctl stop      - Stop server in background
    ./manage.py pg_ctl status    - Check if the server is running
    ./manage.py pg_snapshot foo  - Create a copy of all current database data
    ./manage.py pg_activate foo  - Activate snapshot 'foo'
"""

def activate_clone(snapshot='default'):
    """Activate a certain snapshot by name

    :param snapshot: name of snapshot
    :type snapshot: str
    """
    # TODO: restrict snapshot names to [a-zA-Z0-9_-]+
    if os.pathsep in snapshot or '/' in snapshot:
        raise ValueError("Invalid snapshot name: {0}".format(snapshot))

    snapshot_path = join(ROOT, snapshot)
    if not os.path.isdir(snapshot_path):
        raise OSError("Not a snapshot directory: {0}".format(snapshot_path))

    current_path = join(ROOT, 'current')
    if os.path.exists(current_path):
        os.unlink(current_path)
    os.symlink(snapshot, current_path)


def current_clone():
    return os.readlink(CURRENT).rstrip('/').split('/')[-1]


GET_PORT_RE = re.compile('(^|\n) *port *= *([0-9]+)')
SET_PORT_RE = re.compile('(^|\n)#? *port *= *([0-9]+)')


def get_port():
    """Returns the port the server listens on

    :return: port number
    :rtype: int
    """
    config_path = join(CURRENT, 'postgresql.conf')
    with open(config_path, 'r') as f:
        config = f.read()

    m = GET_PORT_RE.search(config, re.MULTILINE)
    if not m:
        port = 5432
    else:
        port = int(m.group(2))

    return port


def set_port(port):
    """Changes the postgresql config to use given port

    :param port: the port to listen on
    :type port: int
    """
    config_path = join(CURRENT, 'postgresql.conf')
    with open(config_path, 'r') as f:
        config = f.read()

    config = SET_PORT_RE.sub('\\1port = {0}'.format(port), config, re.MULTILINE)

    with open(config_path, 'w') as f:
        f.write(config)


def is_running():
    """Checks if the server is running.

    :return: is running?
    :rtype: bool
    """
    pid_exists = os.path.exists(join(CURRENT, 'postmaster.pid'))
    if pid_exists:
        # Check if really running
        cmd = ['pg_ctl', '-D', CURRENT, 'status']
        p = subprocess.Popen(cmd, bufsize=10000, stdout=subprocess.PIPE)
        output = p.stdout.read()
        #print('pg_ctl status output:', output, file=sys.stderr)
        exitcode = p.wait()
        if exitcode > 0 or not b'pg_ctl: server is running' in output:
            print("PostgreSQL PID file exists, but not running", file=sys.stderr)
            return False
        return True
    else:
        return False


def ensure_stopped(verbose=False):
    """Ensures the database server is not running and stops it if needed.

    :param verbose: If set, info will be printed to stdout
    :type verbose: bool
    :return: indicates if the server was already running
    :rtype: bool
    """
    running = is_running()
    if running:
        if verbose:
            print("PostgreSQL server is running, shutting it down", file=sys.stderr)
        cmd = ['pg_ctl', '-D', CURRENT, '-m', 'fast', 'stop']
        if verbose:
            print(' '.join(cmd), file=sys.stderr)
        subprocess.call(cmd)
        for i in range(20):
            if not is_running():
                break
            time.sleep(0.5)
        if is_running():
            raise Exception("Server still running after 10 seconds")
    return running


def ensure_started(verbose=False):
    """Ensures the database server is running and starts it if needed.

    :param verbose: If set, info will be printed to stdout
    :type verbose: bool
    :return: indicates if the server was already running
    :rtype: bool
    """
    running = is_running()
    if not running:
        if verbose:
            print("PostgreSQL server is not running, starting it", file=sys.stderr)
        cmd = ['pg_ctl', '-D', CURRENT, 'start']
        if verbose:
            print(' '.join(cmd), file=sys.stderr)
        subprocess.call(cmd)
        for i in range(20):
            if is_running():
                break
            time.sleep(0.5)
        if not is_running():
            raise Exception("Server still not running after 10 seconds")
    return running

