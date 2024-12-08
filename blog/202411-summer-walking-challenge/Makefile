include ../../../Makefile.in

## should generate all blog materials
generate-materials: setup-venv main-python clean-venv

## generate figures
main-python:
	. ${VENV_NAME}/bin/activate && python main.py

##! clean generated files
clean-generated-materials:
	rm -rf img/generated
