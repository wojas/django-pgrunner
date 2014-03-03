Introduction
============

Django-pgrunner creates a local PostgreSQL_ database for your project and
automatically starts the database server when needed. It allows you to develop
against a PostgreSQL server, while matching the convenience of a SQLite3
database file.

The local database is a self-contained database created using the PostgreSQL
`initdb` tool. A separate PostgreSQL server will be started on a custom port.

Additionally, it support creating and activating database snapshots. This
allows you to experiment with your data and be confident that you can restore
your old data within seconds.

Requirements and installation
=============================

Make sure you have PostgreSQL_ installed. You can either compile from source,
or install a binary for your operating system. Check the download_ page for
details. For MacOS X users, I recommend downloading PostgresApp_.

The snapshot functionality requires rsync_ to be installed.

The easiest way to install django-pgrunner is using pip:

.. sourcecode:: sh

    pip install django-pgrunner

Microsoft Windows is currently not supported.

**This package is not intended for use on production servers.**

Usage
=====

First, add **pgrunner** to your INSTALLED_APPS.

Next, add the following lines to your `settings.py` or local settings file.
Make sure that these come after any DATABASES setting:

.. sourcecode:: python

    # If your PostgreSQL binaries are not in your path, add this setting
    #PGRUNNER_BIN = '/usr/lib/postgresql/9.3/bin'
    #PGRUNNER_BIN = '/Applications/Postgres.app/Contents/Versions/9.3/bin'

    # This will overwrite DATABASES and auto-start PostgreSQL if needed
    import pgrunner
    pgrunner.settings(locals())

Note that most Linux distibutions do not include these binaries in the PATH,
and only expose a few wrappers in `/usr/bin`. If this is the case for you, you
need to set the `PGRUNNER_BIN` setting.

Run the following command to create your local database:

.. sourcecode:: sh

    ./manage.py pg_init

To start the database in the background:

.. sourcecode:: sh

    ./manage.py pg_ctl start

Note that if you use pgrunner.setting(), it will automatically start the server
for you.

To stop the database:

.. sourcecode:: sh

    ./manage.py pg_ctl stop

This will not be done automatically.

To start the `psql` command line interface with the right parameters, use one of
these commands:

.. sourcecode:: sh

    ./manage.py dbshell
    ./manage.py pg_psql

The only difference is that the first one uses your `DATABASES` settings, and the
second one ignores it.

Snapshots
=========

Snapshots are nothing more than named copies of the full database.
It's the equivalent of a `cp dev.sqlite my-backup.sqlite` for SQLite users.

To create a snapshot and activate it:

.. sourcecode:: sh

    ./manage.py pg_snapshot my-snapshot
    ./manage.py pg_activate my-snapshot

The name of the default snapshot you are running is `default`, so to switch
back:

.. sourcecode:: sh

    ./manage.py pg_activate default

Snapshots can be deleted by removing their folder under `pgrunnerdb/`.

Behind the scenes
=================

Django-pgrunner creates a `pgrunnerdb/` subfolder under your Django project.
This folder contains one folder for every snapshot that was created.
The name of the default instance is `default`. A `current` symbolic link
keeps track of which snapshot is active.

A separate PostgreSQL daemon is started for every project. When the `pg_init`
management command is run, it will pick a random port between 15000 and 16000
to run the server on and write it to the local `postgres.conf`. This way
the chances of a conflict between projects are small.

.. _PostgreSQL: http://www.postgresql.org/
.. _download: http://www.postgresql.org/download/
.. _rsync: http://rsync.samba.org/
.. _PostgresApp : http://postgresapp.com/