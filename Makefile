.PHONY : setup
setup:
	tox -e devenv -v

.PHONY : clean-tox
clean-tox:
	rm -rf devenv .tox

.PHONY : clean-python
clean-python:
	find ./ -name '*.pyc' -delete
	find ./ -name '__pycache__' -delete

.PHONY : clean-package
clean-package:
	rm -rf dist flexer.egg-info

.PHONY : clean
clean: clean-tox clean-python clean-package

.PHONY : test
test:
	tox

.PHONY : package
package: clean-package
	python setup.py sdist

.PHONY : upload
upload: 
	python setup.py sdist upload
