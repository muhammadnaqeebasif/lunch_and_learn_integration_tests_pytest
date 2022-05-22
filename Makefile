.DEFAULT_GOAL := help
.PHONY: build clean format help precommit run setup test
src_dir := src
tests_dir := tests

build: ## Lint and compile code
	poetry run flake8 $(src_dir) $(tests_dir)
	poetry run pylint $(src_dir) $(tests_dir)
	poetry run mypy $(src_dir) $(tests_dir) --strict --show-error-codes
	@echo "Build succeeded"

clean: ## Remove build outputs, test outputs and cached files
	@rm -rf .mypy_cache .pytest_cache .coverage
	@echo "Clean succeeded"

format: ## Reformat source code
	@poetry run isort $(src_dir) $(tests_dir)
	@poetry run black $(src_dir) $(tests_dir)

help: ## Show help message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n"} /^[$$()% 0-9a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

precommit: clean format build test ## Run all checks and tests prior to a commit
	@poetry export --dev --without-hashes --format requirements.txt | poetry run safety check --stdin

run: ## Run the application
	@poetry run python -m django_tutorial

setup:  ## Setup or update local environment
	rm -rf .venv/
	poetry config virtualenvs.in-project true
	poetry install
	pre-commit install

test:  ## Run tests
	@poetry run pytest --cov -m "not(slow)" --durations=5
