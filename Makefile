install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

install-build:
	pip install -r requirements-build.txt

format:
	ruff check --fix
	ruff format

lint:
	ruff check

test:
	pytest -vvv tests

coverage:
	coverage run --source=cloner/ --branch -m pytest tests
	coverage report

FREEZE_OPTIONS = --no-emit-index-url -v
freeze:
	CUSTOM_COMPILE_COMMAND="make freeze" pip-compile $(FREEZE_OPTIONS) -o requirements.txt pyproject.toml
	CUSTOM_COMPILE_COMMAND="make freeze-dev" pip-compile --extra "dev" $(FREEZE_OPTIONS) -o requirements-dev.txt pyproject.toml
	CUSTOM_COMPILE_COMMAND="make freeze-build" pip-compile --extra "build" $(FREEZE_OPTIONS) -o requirements-build.txt pyproject.toml

freeze-upgrade:
	CUSTOM_COMPILE_COMMAND="make freeze" pip-compile $(FREEZE_OPTIONS) -U -o requirements.txt pyproject.toml
	CUSTOM_COMPILE_COMMAND="make freeze-dev" pip-compile --extra "dev" $(FREEZE_OPTIONS) -U -o requirements-dev.txt pyproject.toml
	CUSTOM_COMPILE_COMMAND="make freeze-build" pip-compile --extra "build" $(FREEZE_OPTIONS) -U -o requirements-build.txt pyproject.toml

.PHONY: install install-dev install-build format lint test coverage freeze freeze-upgrade
