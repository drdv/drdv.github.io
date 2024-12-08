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
generate-artifacts:
	cd src/blog && make generate-artifacts

##! clean generated artifacts for all blogs
clean-generated-artifacts:
	cd src/blog && make clean-generated-artifacts

## clean
clean-site:
	rm -rf site
