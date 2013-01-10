#!/usr/bin/env python

from distutils.core import setup

from os.path import abspath, dirname, join
execfile(join(dirname(abspath(__file__)), 'src', 'RequestsLibrary', 'version.py'))

DESCRIPTION = """
Robot Framework keyword library wrapper around the HTTP client library requests.
"""[1:-1]


CLASSIFIERS = """
Development Status :: 5 - Production/Stable
License :: Public Domain
Operating System :: OS Independent
Programming Language :: Python
Topic :: Software Development :: Testing
"""[1:-1]

setup(name         = 'robotframework-requests',
      version      = VERSION,
      description  = 'Robot Framework keyword library wrapper around requests',
      long_description = DESCRIPTION,
      author       = 'Bulkan Savun Evcimen',
      author_email = 'bulkan@gmail.com',
      url          = 'http://github.com/bulkan/robotframework-requests',
      license      = 'Public Domain',
      keywords     = 'robotframework testing test automation http client requests',
      platforms    = 'any',
      classifiers  = CLASSIFIERS.splitlines(),
      package_dir  = {'' : 'src'},
      packages     = ['RequestsLibrary'],
      package_data = {'RequestsLibrary': ['tests/*.txt']},
      install_requires=[
          'requests==0.9.0'
      ],
)

""" From now on use this approach

python setup.py sdist upload
git tag -a 1.2.3 -m 'version 1.2.3'
git push --tags"""
