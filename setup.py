#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import ast
from setuptools import setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('revision_gcs/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')
    ).group(1)))

setup(
    name='revision-gcs',
    version=version,
    packages=['revision_gcs'],
    install_requires=[
        'revision',
        'google-cloud-storage==1.4.0'
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
    ]
)
