include Makefile.inc

.PHONY: serve build artifacts clean-artifacts clean-site clean

## Serve site locally
serve: build
	@$(RUN) mkdocs serve --livereload -o

## Build site
build: clean-site artifacts
	@$(RUN) mkdocs build

## Generate artifacts for all blogs
artifacts:
	@$(MAKE) -C $(BLOG_DIR) all

## Clean generated artifacts for all blogs
clean-artifacts:
	@$(MAKE) -C $(BLOG_DIR) clean

## Clean site
clean-site:
	@rm -rf site

## Clean all
clean: clean-site clean-artifacts
