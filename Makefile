PYTHON=python3
VENV_NAME=.venv

VENV_ACTIVATE=${VENV_NAME}/bin/activate

_BLUE=\033[34m
_END=\033[0m

define show =
	echo -e "${_BLUE}============================================================${_END}" && \
	echo -e "${_BLUE}[$@] ${1}${_END}" && \
	echo -e "${_BLUE}============================================================${_END}"
endef

help: ## show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "${_BLUE}%-12s${_END} %s\n", $$1, $$2}'

serve: build ## serve site locally
	source ${VENV_ACTIVATE} && mkdocs serve

build: clean ## build site
	source ${VENV_ACTIVATE} && mkdocs build

deploy: clean ## deploy site
	source ${VENV_ACTIVATE} && mkdocs gh-deploy

setup-venv: ## setup venv with dependencies
	${PYTHON} -m venv ${VENV_NAME} && \
	. ${VENV_NAME}/bin/activate && \
	pip install --upgrade pip && \
	pip install -r .requirements.txt

clean:
	rm -rf site
