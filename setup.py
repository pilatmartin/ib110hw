from setuptools import setup, find_packages

VERSION = '0.0.1'
AUTHOR = "Martin Pilát"
DESCRIPTION = 'IB110 Homework Library'
LONG_DESCRIPTION = 'A library created for the use in IB110 course at MUNI FI.'

setup(
    name="ib110hw",
    version=VERSION,
    author=AUTHOR,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
)
