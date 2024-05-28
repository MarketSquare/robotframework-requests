#!/usr/bin/env python

import io
from os.path import abspath, dirname, join

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

CLASSIFIERS = """
Development Status :: 5 - Production/Stable
License :: OSI Approved :: MIT License
Operating System :: OS Independent
Programming Language :: Python
Programming Language :: Python :: 3
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Programming Language :: Python :: 3.8
Programming Language :: Python :: 3.9
Topic :: Software Development :: Testing
"""[1:-1]

TEST_REQUIRE = ['robotframework>=3.2.1', 'pytest', 'flask', 'six', 'coverage', 'flake8']

VERSION = None
version_file = join(dirname(abspath(__file__)), 'src', 'RequestsLibrary', 'version.py')
with open(version_file) as file:
    code = compile(file.read(), version_file, 'exec')
    exec(code)

with io.open('README.md', mode='rt', encoding='utf-8') as file:
    readme = file.read()

setup(name='robotframework-requests',
      version=VERSION,
      description='Robot Framework keyword library wrapper around requests',
      long_description=readme,
      long_description_content_type='text/markdown',
      author='Bulkan Savun Evcimen',
      author_email='bulkan@gmail.com',
      maintainer='Luca Giovenzana',
      maintainer_email='luca@giovenzana.org',
      url='https://github.com/MarketSquare/robotframework-requests',
      license='MIT',
      keywords='robotframework testing test automation http client requests rest api',
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
