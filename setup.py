import os
from setuptools import setup, find_packages

version = '0.2.2'

# Will be replaced by the contents of README.rst, if available
desc = """Create and autorun a local PostgreSQL development database for your Django project."""

# This file is not shipped in eggs for some reason..
if os.path.isfile('README.rst'):
    desc = open('README.rst').read()

setup(name='django-pgrunner',
      version=version,
      description="Create and autorun a PostgreSQL development database for your Django project",
      long_description=desc,
      classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Topic :: Database',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
      ], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='django postgres postgresql runner pgrunner',
      author='Konrad Wojas',
      author_email='konrad@wojas.nl',
      url='https://github.com/wojas/django-pgrunner/',
      license='LICENSE',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests', 'test_project']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'Django >= 1.4',
        #'psycopg2' -- not really required by this package, but required by Django
      ],
      entry_points="""
      """,
      )
