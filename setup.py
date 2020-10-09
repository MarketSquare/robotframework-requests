#!/usr/bin/env python

import sys
from os.path import abspath, dirname, join

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


PY3 = sys.version_info > (3,)

VERSION = None
version_file = join(dirname(abspath(__file__)), 'src', 'RequestsLibrary', 'version.py')
with open(version_file) as file:
    code = compile(file.read(), version_file, 'exec')
    exec(code)

DESCRIPTION = """
Robot Framework keyword library wrapper around the HTTP client library requests.
"""[1:-1]

CLASSIFIERS = """
Development Status :: 5 - Production/Stable
License :: OSI Approved :: MIT License
Operating System :: OS Independent
Programming Language :: Python
Topic :: Software Development :: Testing
"""[1:-1]

TEST_REQUIRE = ['robotframework>=3.2.1', 'pytest', 'flask', 'coverage', 'flake8'] if PY3 \
    else ['robotframework>=3.2.1', 'pytest', 'flask', 'coverage', 'flake8', 'mock']

setup(name='robotframework-requests',
      version=VERSION,
      description='Robot Framework keyword library wrapper around requests',
      long_description=DESCRIPTION,
      author='Bulkan Savun Evcimen',
      author_email='bulkan@gmail.com',
      maintainer='Luca Giovenzana',
      maintainer_email='luca@giovenzana.org',
      url='http://github.com/bulkan/robotframework-requests',
      license='MIT',
      keywords='robotframework testing test automation http client requests',
      platforms='any',
      classifiers=CLASSIFIERS.splitlines(),
      package_dir={'': 'src'},
      packages=['RequestsLibrary'],
      install_requires=[
          'robotframework',
          'requests'
      ],
      extras_require={
          'test': TEST_REQUIRE
      })
