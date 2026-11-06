PYTHON ?= python3

.PHONY: setup validate-repository web web-checks checks

setup:
	@$(PYTHON) -c 'import sys; print("Python environment OK:", sys.version.split()[0])'

validate-repository:
	$(PYTHON) scripts/validate_repository.py

web:
	$(PYTHON) web/build.py

web-checks:
	$(PYTHON) web/build.py --check
	$(PYTHON) -m unittest discover -s web/tests

checks: setup validate-repository web-checks
	@echo "Repository checks complete."
