from pip.req import parse_requirements
from setuptools import setup, find_packages
import uuid
import os

requirements = parse_requirements('requirements.txt', session=uuid.uuid1())
install_requires = [str(r.req) for r in requirements]

# workaround for hard links breaking virtualbox build on ubuntu
# http://bugs.python.org/issue8876#msg208792
del os.link

setup(
    name="flexer",
    version="1.0.0",
    url='http://www.ntt.com',
    author='NTT communications',
    author_email='minder@nexus.ntteo.net',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=install_requires,
    entry_points='''
        [console_scripts]
        flexer=flexer.cli:cli
    ''',
)
