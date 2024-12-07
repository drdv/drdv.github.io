PYTHON=python
VENV_NAME=.venv
VENV_ACTIVATE=${VENV_NAME}/bin/activate

HELP_SCRIPT=$(HOME)/local/bi/

## show this help
help:
	@awk -f scripts/makefile-help-target.awk $(MAKEFILE_LIST)

## serve site locally
serve: build
	source ${VENV_ACTIVATE} && mkdocs serve

## build site
build: clean
	source ${VENV_ACTIVATE} && mkdocs build

##! deploy site
deploy: clean
	source ${VENV_ACTIVATE} && mkdocs gh-deploy

## setup venv with dependencies
setup-venv:
	${PYTHON} -m venv ${VENV_NAME} && \
	. ${VENV_NAME}/bin/activate && \
	pip install --upgrade pip && \
	pip install -r .requirements.txt

## clean
clean:
	rm -rf site
