.PHONY: test-services clean lint type-check

test-services:
	python -m undetectable_bot.test_services

clean:
	rm -rf data/*
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

format-py:
	ruff format .

format-js:
	npx prettier --write "undetectable_bot/js/**/*.js"

format: format-py format-js

lint-py:
	ruff . --fix

lint-js:
	npx eslint "undetectable_bot/js/**/*.js" --fix

lint: lint-py lint-js

type-check:
	mypy .

all: clean lint format type-check test-services 