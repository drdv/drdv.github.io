include ../../../Makefile.in

## generates all blog artifacts
generate-artifacts: setup-venv main-python clean-venv

## generate figures
main-python:
	. ${VENV_NAME}/bin/activate && python main.py

##! clean generated files
clean-generated-artifacts:
	rm -rf img/generated
