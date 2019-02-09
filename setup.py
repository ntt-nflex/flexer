from setuptools import setup, find_packages
import os
import re


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


install_requires = parse_requirements('requirements.txt')
description = ("Flexer is a command line tool for interacting with nFlex "
               "and running nFlex modules locally.")
with open('README.md') as f:
    long_description = f.read()

# workaround for hard links breaking virtualbox build on ubuntu
# http://bugs.python.org/issue8876#msg208792
# del os.link

with open(
        os.path.join(
            os.path.dirname(__file__),
            'flexer', '__init__.py')) as v_file:
    VERSION = re.compile(
        r".*__version__ = '(.*?)'",
        re.S).match(v_file.read()).group(1)

setup(
    name="flexer",
    version=VERSION,
    description=description,
    long_description=long_description,
    url='http://www.ntt.com',
    author='NTT communications',
    author_email='minder@nexus.ntteo.net',
    licence='GNU General Public License v2 (GPLv2)',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=install_requires,
    entry_points='''
        [console_scripts]
        flexer=flexer.cli:cli
    ''',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development',
    ],
)
