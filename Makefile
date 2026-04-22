# Convenience wrapper so `make` works from `repo/`.
# Delegates to the top-level slide build Makefile.

TOP_MAKE := ../Makefile

.DEFAULT_GOAL := all-slides

.PHONY: all all-slides

all all-slides:
	$(MAKE) -f $(TOP_MAKE) MODULE="$(MODULE)" $@

%:
	$(MAKE) -f $(TOP_MAKE) MODULE="$(MODULE)" $@
