#!/usr/bin/env python
# -*- coding: UTF-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name="ugoira_conv",
    version="0.2.0",
    description="ugoira converter",
    long_description="convert ugoira (pixiv animations) to webm or gif",
    url="https://github.com/mikf/ugoira-conv",
    author="Mike Fährmann",
    author_email="mike_faehrmann@web.de",
    license="GPLv2",
    scripts=[
        "bin/ugoira-conv",
    ],
    entry_points={
        'console_scripts': [
            'ugoira-conv = ugoira_conv:main',
        ],
    },
    packages=[
        "ugoira_conv",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Multimedia :: Video :: Conversion",
    ],
)
