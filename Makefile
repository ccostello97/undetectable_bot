.PHONY: test-services clean lint type-check

test-services:
	python -m undetectable_bot.utils.test_services

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
	ruff check --fix .

lint-js:
	npx eslint --fix "undetectable_bot/js/**/*.js"

lint: lint-py lint-js

type-check:
	mypy .

all: clean lint format type-check test-services