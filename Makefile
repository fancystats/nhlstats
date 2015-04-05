SHELL=/bin/bash
PYTHON=`which python`
NAME=`python setup.py --name`
VERSION=`python setup.py --version`
SDIST=dist/$(NAME)-$(VERSION).tar.gz

# Fixes clang compile errors
ARCHFLAGS=-Wno-error=unused-command-line-argument-hard-error-in-future

all: check test source deb

dist: source deb

source:
	$(PYTHON) setup.py sdist

deb:
	$(PYTHON) setup.py --command-packages=stdeb.command bdist_deb

rpm:
	$(PYTHON) setup.py bdist_rpm --post-install=rpm/postinstall --pre-uninstall=rpm/preuninstall

install:
	$(PYTHON) setup.py install --install-layout=deb

develop:
	$(PYTHON) setup.py develop

test: venv develop
	source venv/bin/activate && nosetests

check: venv
	source venv/bin/activate && find . -name \*.py -not -path "./venv*" | grep -v "_tests.py$" | xargs pylint --errors-only --reports=n --generated-members=name

cache-index:
	echo > cache/index.html && find cache/* | grep -v index.html | cut -d / -f 2 | xargs -I {} echo "<a href=\"{}\">{}</a><br />" >> cache/index.html

venv:
	test -d venv || virtualenv venv
	source venv/bin/activate && pip install --quiet --use-wheel -r requirements.txt

init: clean venv

daily:
	$(PYTHON) setup.py bdist egg_info --tag-date

deploy:
	# make sdist
	rm -rf dist
	python setup.py sdist

	# setup venv
	rm -rf $(VENV)
	virtualenv --no-site-packages $(VENV)
	$(VENV)/bin/pip install $(SDIST)

clean:
	$(PYTHON) setup.py clean
	rm -rf build/ MANIFEST dist build nhlstats.egg-info deb_dist venv cache
	find . -name '*.pyc' -delete
