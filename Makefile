PYTHON = python3
ENTRY_POINT = a_maze_ing.py
CONFIG_FILE = config.txt

.PHONY: all run debug clean lint lint-strict test help

all: run

install:
	pip install -r requirements.txt

run:
	$(PYTHON) $(ENTRY_POINT) $(CONFIG_FILE)

debug:
	$(PYTHON) -m pdb $(ENTRY_POINT) $(CONFIG_FILE)

clean:
	rm -rf __pycache__ .mypy_cache .pytest_cache build dist *.egg-info
	rm -f maze.txt

lint:
	flake8 .
	mypy --strict .

test:
	$(PYTHON) -m unittest discover -s tests
