# -*- coding: utf-8 -*-
__author__ = 'Christoph Hauzenberger'

import os
from setuptools import setup, find_packages

def read_file(filename):
    """Read a file into a string"""
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        return open(filepath).read()
    except IOError:
        return ''

setup(name='battleship_server',
      version = __import__('server').__version__.replace(' ', '-'),
      author = 'Chris Hauzenberger',
      author_email = 'christoph.hauzenberger@namics.com',
      install_requires = read_file('requirements.txt'),
      packages = find_packages(),
      test_suite='nose.collector',
      test_requires=['nose', 'mock'],
      include_package_data = True,
      package_data = {
        '': ['*.csv', '*.xml', '*.ContentValue', '*.cnd'],
            'result_generator':
                         []
      },
      entry_points = {
          'console_scripts': [
              'battleship_server = server.main:main',
          ],
      },
)
