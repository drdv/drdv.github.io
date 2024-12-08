include Makefile.in

## serve site locally
serve: build
	source ${VENV_ACTIVATE} && mkdocs serve

## build site
build: clean-site
	source ${VENV_ACTIVATE} && mkdocs build

##! deploy site
deploy: clean-site
	source ${VENV_ACTIVATE} && mkdocs gh-deploy

## generate data for all blogs
generate-materials:
	cd src/blog && make generate-materials

##! clean generated materials for all blogs
clean-generated-materials:
	cd src/blog && make clean-generated-materials

## clean
clean-site:
	rm -rf site
