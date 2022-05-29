.PHONY: build test cover publish run clean

build:
	python3 -m build

test:
	pytest

cover:
	coverage run --source=src -m pytest
	coverage html
	open htmlcov/index.html

publish:
	python3 -m twine upload --repository pypi dist/*

run:
	cd src; python3 -m clock_tracking

clean:
	rm -rf dist
	rm -rf src/clock_tracking/__pycache__
	rm -rf src/clock_tracking_tests/__pycache__
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf .pytest_cache