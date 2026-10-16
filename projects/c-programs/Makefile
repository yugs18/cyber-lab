CC := gcc
CFLAGS := -std=c11 -Wall -Wextra -Wpedantic -g

PROGRAMS_DIR := programs

.PHONY: list clean help

# Build a program by name: make array_max
%:
	@if [ -f "$(PROGRAMS_DIR)/$@/$@.c" ]; then \
		$(CC) $(CFLAGS) "$(PROGRAMS_DIR)/$@/$@.c" \
			-o "$(PROGRAMS_DIR)/$@/$@"; \
	else \
		echo "Unknown program: $@"; \
		echo "Run 'make list' to see available programs."; \
		exit 1; \
	fi

list:
	@find $(PROGRAMS_DIR) -mindepth 2 -maxdepth 2 \
		-type f -name '*.c' \
		-print | sed 's|$(PROGRAMS_DIR)/||; s|/[^/]*\.c$$||' | sort

clean:
	@find $(PROGRAMS_DIR) -mindepth 2 -maxdepth 2 \
		-type f -executable ! -name '*.c' -delete
	@echo "Compiled executables removed."

help:
	@echo "make array_max   Build array_max"
	@echo "make fork        Build fork"
	@echo "make list        List available programs"
	@echo "make clean       Remove compiled executables"