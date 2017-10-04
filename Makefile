
install:
	pip install -q .

install-dev:
	pip install -q -e .[dev]

lint:
	flake8 .

test:
	pytest
