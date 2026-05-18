.PHONY: help check lint test docs clean

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

check: ## Run static type checking on the Python code
	@poetry run pyright

lint: ## Run linting on the Python code
	@poetry run ruff check

test: ## Run repository tests
	@poetry run python -m test.rdfoo

docs: ## Build the documentation
	@poetry run sphinx-build -E -a -b html ./docs/source ./docs/build/html

clean: ## Clean documentation artifacts
	-rm -r ./docs/source/modules
	-rm -r ./docs/build
