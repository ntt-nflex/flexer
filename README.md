flexer
======

Flexer is a command line tool for interacting with nFlex and running nFlex modules locally.

Installation
------------

Install, upgrade and uninstall flexer with these commands:
```sh
$ pip install flexer
$ pip install --upgrade flexer
$ pip uninstall flexer
```
or fork this repository

Dependencies
------------

The flexer tool is supported on Python 2.7.

The main dependencies are:
* [requests]: HTTP for Humans
* [click]: for creating beautiful command line interfaces
* [jsonschema]: an implementation of JSON Schema for Python
* [jinja2]: modern and designer-friendly templating language for Python
* [pyyaml]: YAML parser and emitter for Python

The testing dependencies are:
* [pytest]: helps you write better programs
* [mock]: a library for testing in Python

Testing
-------

Make sure you have [tox] by running the following:
```sh
$ pip install tox
```

To run the package tests:
```sh
$ tox
```
or
```sh
$ make test
```

Bash Completion
---------------
For detailed explanation on how to enable bash completion for the flexer script, please read the [click documentation](http://click.pocoo.org/5/bashcomplete/).

Basically you need to run
```sh
_FLEXER_COMPLETE=source flexer > ~/flexer-complete.sh
```
and add this line to your `.bashrc` file:
```sh
source ~/flexer-complete.sh
```

License
-------

[GNU General Public License, version 2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)

[//]: #
   [requests]: <http://docs.python-requests.org>
   [click]: <http://click.pocoo.org>
   [jsonschema]: <https://python-jsonschema.readthedocs.io/en/latest/>
   [jinja2]: <http://jinja.pocoo.org>
   [pyyaml]: <http://pyyaml.org/wiki/PyYAML>
   [mock]: <https://pypi.python.org/pypi/mock>
   [pytest]: <http://doc.pytest.org>
   [tox]: <https://tox.readthedocs.io/>

