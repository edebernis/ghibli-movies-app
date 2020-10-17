# -*- coding: utf-8 -*-

import re
from setuptools import setup, find_packages


version = re.search(r'^__version__\s*=\s*"(.*)"',
                    open('ghibli/app.py').read(), re.M) \
            .group(1)


with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")


setup(
    name="ghibli-movies",
    packages=find_packages(),
    version=version,
    description="uWSGI application to list movies produced by Ghibli studios",
    long_description=long_descr,
    author="Emeric de Bernis",
    author_email="emeric.debernis@gmail.com",
    install_requires=[
        'bottle>=0.12.18'
    ],
    tests_require=[
        'pytest>=5.4.1',
        'mock>=4.0.2',
        'webtest>=2.0.35'
    ]
)
