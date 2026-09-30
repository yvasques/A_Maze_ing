PYTHON = python3
CONFIG_FILE = config.txt
VENV = .venv
PIP = $(VENV)/bin/pip
PYTHON_VENV = $(VENV)/bin/python
ENTRY_POINT = a_maze_ing.py

.PHONY: install run debug clean lint lint-strict

install:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install flake8 mypy

run:
	$(PYTHON_VENV) $(ENTRY_POINT) $(CONFIG_FILE)

debug:
	$(PYTHON_VENV) -m pdb $(ENTRY_POINT) $(CONFIG_FILE)

clean:
	rm -rf __pycache__ .mypy_cache .pytest_cache build dist *.egg-info $(VENV)

lint:
	$(PYTHON_VENV) -m flake8 --exclude=$(VENV) .
	$(PYTHON_VENV) -m mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	$(PYTHON_VENV) -m flake8 --exclude=$(VENV) .
	$(PYTHON_VENV) -m mypy --strict --exclude $(VENV) .
