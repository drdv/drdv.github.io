PYTHON=python
PIP=pip
VENV_NAME=.venv

all:
	echo "be reasonable, check available targets"

setup-venv: # setup venv with dependencies
	${PYTHON} -m venv ${VENV_NAME} && \
	. ${VENV_NAME}/bin/activate && \
	${PIP} install --upgrade pip && \
	${PIP} install -r .requirements.txt
