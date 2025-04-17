.PHONY: test-services clean lint type-check

test-services:
	python -m undetectable_bot.test_services

clean:
	rm -rf data/*
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

lint:
	ruff check .
	ruff format .

type-check:
	mypy .

all: clean lint type-check test-services 