-include $(HOME)/help.mk

MAKEFLAGS := --no-print-directory --warn-undefined-variables
LEDGER := ledger
LEDGER_DEPS := data.ledger .ledgerrc

override OUT_DIR := out

empty :=
space := $(empty) $(empty)
ARTIFACTS := bal-backbone bal-vegetables bal-proteins bal-carbs bal-fruits bal-fats reg-eggs
MAKEFILE_DOC_FLAGS := -v SUB='$(subst $(space),;,$(foreach t,$(ARTIFACTS),$$(OUT_DIR)/$t:$(OUT_DIR)/$t:))'

.PHONY: all clean

## Generate artifacts
all: $(addprefix $(OUT_DIR)/,$(ARTIFACTS))

## Balance: backbone
$(OUT_DIR)/bal-backbone: $(LEDGER_DEPS) Makefile | $(OUT_DIR)
	@$(LEDGER) bal Legumes Grains Nuts --no-total > $@

## Balance: vegetables
$(OUT_DIR)/bal-vegetables: $(LEDGER_DEPS) Makefile | $(OUT_DIR)
	@$(LEDGER) bal Vegetables --no-total > $@

## Balance: proteins
$(OUT_DIR)/bal-proteins: $(LEDGER_DEPS) Makefile | $(OUT_DIR)
	@$(LEDGER) bal Proteins --no-total > $@

## Balance: carbs
$(OUT_DIR)/bal-carbs: $(LEDGER_DEPS) Makefile | $(OUT_DIR)
	@$(LEDGER) bal Carbs --no-total > $@

## Balance: carbs
$(OUT_DIR)/bal-fruits: $(LEDGER_DEPS) Makefile | $(OUT_DIR)
	@$(LEDGER) bal Fruits --no-total > $@

## Balance: fats
$(OUT_DIR)/bal-fats: $(LEDGER_DEPS) Makefile | $(OUT_DIR)
	@$(LEDGER) bal Fats --no-total > $@

## Register: eggs
$(OUT_DIR)/reg-eggs: $(LEDGER_DEPS) Makefile | $(OUT_DIR)
	@$(LEDGER) reg Eggs -W --payee-width 15 --account-width 25 --amount-width 10 > $@

$(OUT_DIR):
	@mkdir -p $@

clean:
	@rm -rf $(OUT_DIR)
