-include $(HOME)/help.mk

DEPS =
VFLAGS =

BLOG_DIR := src/blog
MAKEFLAGS := --no-print-directory --warn-undefined-variables --no-builtin-rules
RUN = uv run --with=$(DEPS)

