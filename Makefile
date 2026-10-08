PYTHON = python3
CONFIG_FILE = config.txt
VENV = .venv
PIP = $(VENV)/bin/pip
PYTHON_VENV = $(VENV)/bin/python
ENTRY_POINT = a_maze_ing.py

MLX_ARCHIVE = mlx-2.2.tgz
MLX_DIR = .mlx_src
DISTRO := $(shell if grep -qi '^ID=fedora' /etc/os-release 2>/dev/null; \
	then echo fedora; else echo ubuntu; fi)
MLX_WHEEL = $(MLX_DIR)/$(DISTRO)/mlx-2.2-py3-none-any.whl

.PHONY: install run debug build clean lint lint-strict

install:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install flake8 mypy build
	rm -rf $(MLX_DIR)
	mkdir -p $(MLX_DIR)
	tar -xzf $(MLX_ARCHIVE) -C $(MLX_DIR)
	$(PIP) install $(MLX_WHEEL)

run:
	$(PYTHON_VENV) $(ENTRY_POINT) $(CONFIG_FILE)

debug:
	$(PYTHON_VENV) -m pdb $(ENTRY_POINT) $(CONFIG_FILE)

build:
	$(PYTHON_VENV) -m build --wheel --outdir .
	rm -rf build *.egg-info

clean:
	rm -rf __pycache__ .mypy_cache .pytest_cache \
	build dist *.egg-info $(VENV) $(MLX_DIR)

lint:
	$(PYTHON_VENV) -m flake8 --exclude=$(VENV),$(MLX_DIR),build,dist .
	$(PYTHON_VENV) -m mypy . \
		--exclude '$(MLX_DIR)|build|dist' \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	$(PYTHON_VENV) -m flake8 --exclude=$(VENV),$(MLX_DIR),build,dist .
	$(PYTHON_VENV) -m mypy --strict --exclude '$(VENV)|$(MLX_DIR)|build|dist' .
