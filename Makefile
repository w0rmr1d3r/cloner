install:
	pip install -r requirements.txt

install-dev: install
	pip install -e ".[dev]"

format:
	isort --float-to-top .
	black .

lint: isort-lint black-lint flake8-lint

isort-lint:
	isort --check-only .

black-lint:
	black --check .

flake8-lint:
	flake8 .

unit:
	pytest -svvv tests

test: lint unit

freeze:
	CUSTOM_COMPILE_COMMAND="make freeze" pip-compile --no-emit-index-url -v --output-file requirements.txt setup.py --max-rounds 50

freeze-upgrade:
	CUSTOM_COMPILE_COMMAND="make freeze" pip-compile --no-emit-index-url -v --upgrade --output-file requirements.txt setup.py --max-rounds 50

build: install-dev test

.PHONY: build install install-dev isort-lint black-lint flake8-lint format unit test freeze freeze-upgrade
