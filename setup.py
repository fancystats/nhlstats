#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]

# Bring __version__ into the current scope
__version__ = None  # Predeclare to make linters happy.
execfile('nhlstats/version.py')

setup(name='nhlstats',
      version=__version__,
      author='Jim Kelly',
      author_email='pthread1981@gmail.com',
      url='http://www.fancystats.org',
      description='The nhlstats program retrieves game data from the NHL.',
      long_description='One can use nhlstats to retrieve game data from the NHL for storage in a local database for later analysis.',
      packages=find_packages(),
      include_package_data=True,
      package_data={'': ['*.txt', '*.rst']},
      exclude_package_data={'': ['README.txt']},
      scripts=['bin/nhlstats'],
      keywords='python tools utils nhl stats fancystats',
      license='MIT',
      install_requires=REQUIREMENTS,)
