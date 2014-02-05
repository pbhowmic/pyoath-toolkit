#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import find_packages, setup
import sys

os.environ['SETUP_PY'] = '1'

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from oath_toolkit import metadata

with open('README.rst') as f:
    long_description = f.read()

requires = []
if not os.environ.get('READTHEDOCS'):
    requires = [l for l in open('requirements.txt')]
extras_require = {}
for extra in ['django-otp', 'qrcode', 'wtforms']:
    req_txt = 'requirements-{0}.txt'.format(extra)
    extras_require[extra] = [l for l in open(req_txt)]

setup(name='pyoath-toolkit',
      version=metadata.VERSION,
      description=metadata.DESCRIPTION,
      long_description=long_description,
      author='Mark Lee',
      author_email='pyoath-toolkit@lazymalevolence.com',
      url='https://pyoath-toolkit.readthedocs.org/',
      packages=find_packages(),
      install_requires=requires,
      extras_require=extras_require,
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: POSIX',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: Implementation :: PyPy',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ])
