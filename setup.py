#!/usr/bin/env python
# coding=utf-8

import os
import re
from distutils.core import setup

VERSION = None
with open(os.path.join(os.path.dirname(__file__), 'heap', '__init__.py')) as fp:
    _r = re.compile(r'''^__version__\s*=\s*(['"])(.*?)\1(?:\s;)*$''')
    for line in fp:
        match = _r.match(line)
        if match:
            VERSION = match.group(2)
if VERSION is None:
    raise ValueError('Unable to find package version')

setup(
    name='pyheap',
    packages=['heap'],
    version=VERSION,
    description='heap implementation based on heapq',
    author='Brandon LeBlanc',
    author_email='demosdemon@gmail.com',
    url='https://github.com/demosdemon/pyheap',
    download_url='https://github.com/demosdemon/pyheap/tarball/%s' % VERSION,
    keywords=['heap'],
    classifiers=[],
)
