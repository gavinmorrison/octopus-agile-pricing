.PHONY: help install test lint clean run example setup dev-install

help:
	@echo "Available commands:"
	@echo "  setup        - Set up development environment"
	@echo "  install      - Install dependencies"
	@echo "  dev-install  - Install in development mode"
	@echo "  test         - Run tests"
	@echo "  lint         - Run linting"
	@echo "  run          - Run the main script (London, 7 days)"
	@echo "  run-yorkshire- Run script for Yorkshire (3 days)"
	@echo "  list-regions - List all available regions"
	@echo "  example      - Run example script"
	@echo "  clean        - Clean up generated files"

setup: 
	python3 -m venv .venv
	@echo "Virtual environment created. Activate with:"
	@echo "source .venv/bin/activate"

install:
	pip install -r requirements.txt

dev-install:
	pip install -r requirements.txt
	pip install pytest pytest-cov flake8 black isort

test:
	python -m pytest tests/ -v

lint:
	flake8 octopus_agile_prices.py examples/ tests/
	black --check octopus_agile_prices.py examples/ tests/

format:
	black octopus_agile_prices.py examples/ tests/
	isort octopus_agile_prices.py examples/ tests/

run:
	python octopus_agile_prices.py

run-yorkshire:
	python octopus_agile_prices.py --region Yorkshire --days 3

list-regions:
	python octopus_agile_prices.py --list-regions

example:
	python examples/basic_usage.py

clean:
	rm -rf output/
	rm -rf __pycache__/
	rm -rf tests/__pycache__/
	rm -rf examples/__pycache__/
	rm -rf .pytest_cache/
	rm -rf *.egg-info/
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
