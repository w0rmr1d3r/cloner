install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

format:
	isort --float-to-top .
	black .
	docformatter --in-place --recursive .

lint:
	isort --check-only .
	black --check .
	docformatter --check --recursive .
	flake8 .

unit:
	pytest -svvv tests

test: lint unit

coverage:
	coverage run --source=cloner/ --branch -m pytest tests --junitxml=build/test.xml -v
	coverage xml -i -o build/coverage.xml
	coverage report

py-lint:
	pylint cloner/

py-lint-test:
	# C0116 - missing function docstring - does not apply to tests
	pylint --disable=C0116 tests/

freeze:
	CUSTOM_COMPILE_COMMAND="make freeze" pip-compile --no-emit-index-url -v -o requirements.txt pyproject.toml
	CUSTOM_COMPILE_COMMAND="make freeze-dev" pip-compile --extra "dev" --no-emit-index-url -v -o requirements-dev.txt pyproject.toml

freeze-upgrade:
	CUSTOM_COMPILE_COMMAND="make freeze" pip-compile --upgrade --no-emit-index-url -v -o requirements.txt pyproject.toml
	CUSTOM_COMPILE_COMMAND="make freeze-dev" pip-compile --extra "dev" --upgrade --no-emit-index-url -v -o requirements-dev.txt pyproject.toml

.PHONY: install install-dev format lint unit test coverage freeze freeze-upgrade py-lint py-lint-test
