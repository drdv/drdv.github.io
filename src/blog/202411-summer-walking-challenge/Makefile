include ../../../Makefile.inc

ARTIFACTS := artifacts

.PHONY: all clean

## Generate artifacts
all: DEPS := pandas,matplotlib
all: $(ARTIFACTS)/.done

## Clean artifacts
clean:
	@rm -rf $(ARTIFACTS)

$(ARTIFACTS)/.done: main.py
	@$(RUN) main.py -o $(ARTIFACTS)
	@touch $@
