PYTHON=python
VENV_NAME=.venv
VENV_ACTIVATE=${VENV_NAME}/bin/activate

## show this help
help:
	-@awk -f makefile-help-target.awk $(MAKEFILE_LIST)

## serve site locally
serve: build
	source ${VENV_ACTIVATE} && mkdocs serve

## build site
build: clean
	source ${VENV_ACTIVATE} && mkdocs build

##! deploy site
deploy: clean
	source ${VENV_ACTIVATE} && mkdocs gh-deploy

## generate data for all blogs
generate-data:
	cd src/blog && make main

##! clean generated files for all blogs
clean-generated:
	cd src/blog && make clean-generated

## setup venv with dependencies
setup-venv:
	${PYTHON} -m venv ${VENV_NAME} && \
	. ${VENV_NAME}/bin/activate && \
	pip install --upgrade pip && \
	pip install -r .requirements.txt

## clean
clean:
	rm -rf site
