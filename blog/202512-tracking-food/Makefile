MAKEFLAGS := --no-print-directory --warn-undefined-variables
LEDGER := ledger
LEDGER_DEPS := data.ledger .ledgerrc

override OUT_DIR := out

EXPORT_BALANCE := balance

help: URL := github.com/drdv/makefile-doc/releases/latest/download/makefile-doc.awk
help: DIR := $(HOME)/.local/share/makefile-doc
help: SCR := $(DIR)/makefile-doc.awk
help: VFLAGS = -v SUB='$$(OUT_DIR)/$$(EXPORT_BALANCE):$(OUT_DIR)/$(EXPORT_BALANCE):'
help: ## Show this help
	@test -f $(SCR) || wget -q -P $(DIR) $(URL)
	@awk $(VFLAGS) -f $(SCR) $(MAKEFILE_LIST)

.PHONY: all clean

## Generate artifacts
all: \
	$(OUT_DIR)/bal-backbone \
	$(OUT_DIR)/bal-vegetables \
	$(OUT_DIR)/bal-proteins \
	$(OUT_DIR)/bal-carbs \
	$(OUT_DIR)/bal-fruits \
	$(OUT_DIR)/bal-fats \
	$(OUT_DIR)/reg-eggs

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
