include Makefile.in

BLOG_DIR := src/blog
MAKEFLAGS := --no-print-directory

## Serve site locally
serve: build
	@$(RUN) mkdocs serve --livereload -o

## Build site
build: clean-site artifacts-generate
	@$(RUN) mkdocs build

##! Deploy site
deploy: clean-site
	@${RUN} mkdocs gh-deploy

## Generate artifacts for all blogs
artifacts-generate:
	@cd $(BLOG_DIR) && $(MAKE) artifacts-generate

## Clean generated artifacts for all blogs
artifacts-clean:
	@cd $(BLOG_DIR) && $(MAKE) artifacts-clean

## Clean site
clean-site:
	@rm -rf site

## Clean all
clean: clean-site artifacts-clean
