include ../../../Makefile.in

OUT_DIR := img/generated

## Generate artifacts
artifacts-generate: DEPS := pandas,matplotlib
artifacts-generate: $(OUT_DIR)/.done

## Clean generated artifacts
artifacts-clean:
	@rm -rf $(OUT_DIR)

$(OUT_DIR)/.done: main.py
	@$(RUN) main.py -o $(OUT_DIR)
	@touch $@
