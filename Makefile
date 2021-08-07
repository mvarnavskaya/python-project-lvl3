install:
	poetry install

build:
	poetry build
	python3 -m pip install --user dist/*.whl
	
lint:
	poetry run flake8 page_loader
	poetry run flake8 tests

test:
	poetry run pytest -v

test-coverage:
	poetry run pytest --cov=page_loader --cov-report xml tests/

