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
    description='Google Cloud Storage for Revision',
    author='SENSY Inc.',
    url='https://github.com/COLORFULBOARD/revision-gcs',
    license='MIT',
    packages=['revision_gcs'],
    install_requires=[
        'revision',
        'google-cloud-storage==1.4.0'
    ],
    extras_require={
        'dev': [
            'flake8==3.4.1',
            'pytest==3.2.2'
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
