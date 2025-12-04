include ../../Makefile.inc

POST_DIRS := \
	202411-summer-walking-challenge \
	202512-tracking-food

POST_TARGETS_ALL := $(POST_DIRS:%=%-all)
POST_TARGETS_CLEAN := $(POST_DIRS:%=%-clean)

.PHONY: all clean $(POST_TARGETS_ALL) $(POST_TARGETS_CLEAN)

## Generate artifacts for all posts
all: $(POST_TARGETS_ALL)

## Clean artifacts for all posts
clean: $(POST_TARGETS_CLEAN)

$(POST_TARGETS_ALL):
	@$(MAKE) -C ${@:-all=} all

$(POST_TARGETS_CLEAN):
	@$(MAKE) -C ${@:-clean=} clean
