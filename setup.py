#!/usr/bin/env python3

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cicspi",
    version="0.1.0",
    author="Carsten Wulff",
    author_email="carsten@wulff.no",
    description="Spice toolbox",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wulffern/cicspi",
    packages=setuptools.find_packages(),
    python_requires='>=3.8',
    entry_points = {'console_scripts': [
        'cicspi = cicspi.entry:cli',
    ]},
    install_requires = 'click'.split(),
    classifiers = [
        'Development Status :: 1 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        "License :: OSI Approved :: MIT License",
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.8',
        'Topic :: Utilities',
        'Topic :: Scientific/Engineering',
    ],
)
