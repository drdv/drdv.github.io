PYTHON=python
PIP=pip
VENV_NAME=.venv

all:
	echo "be reasonable, check available targets"

main: setup-venv main-python clean-venv

main-python:
	. ${VENV_NAME}/bin/activate && python main.py

freeze:
	@pipdeptree -f -d 0 -w silence | grep -v 'pipdeptree' > .requirements.txt

setup-venv: # setup venv with dependencies
	${PYTHON} -m venv ${VENV_NAME} && \
	. ${VENV_NAME}/bin/activate && \
	${PIP} install --upgrade pip && \
	${PIP} install -r .requirements.txt

clean-generated:
	rm -rf img/generated

clean-venv:
	rm -rf .venv
