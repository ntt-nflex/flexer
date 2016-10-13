from pip.req import parse_requirements
from setuptools import setup, find_packages
import uuid
import os

requirements = parse_requirements('requirements.txt', session=uuid.uuid1())
install_requires = [str(r.req) for r in requirements]
description = ("Flexer is a command line tool for interacting with nFlex "
               "and running nFlex modules locally.")
with open('README.md') as f:
    long_description = f.read()

# workaround for hard links breaking virtualbox build on ubuntu
# http://bugs.python.org/issue8876#msg208792
del os.link

setup(
    name="flexer",
    version="1.0.3",
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
        'Programming Language :: Python :: 2 :: Only',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development',
    ],
)
