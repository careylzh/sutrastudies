PYTHON ?= python3

.PHONY: setup validate-repository checks

setup:
	@$(PYTHON) -c 'import sys; print("Python environment OK:", sys.version.split()[0])'

validate-repository:
	$(PYTHON) scripts/validate_repository.py

checks: setup validate-repository
	@echo "Repository checks complete."
