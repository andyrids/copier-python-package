.DEFAULT_GOAL := help

.PHONY: help secrets-baseline setup

all: help

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "%-20s %s\n", $$1, $$2}'

secrets-baseline: ## Generate a detect-secrets baseline for the repository
	@echo "Creating secrets baseline..."
	@uv run detect-secrets scan --exclude-files '(\.secrets\.baseline|.*\.lock)' > .secrets.baseline

setup: ## Setup development environment
	@echo "Creating development environment..."
	@uv sync
	@echo "Creating pre-commit hooks..."
	@uv run -m prek install
	@$(MAKE) secrets-baseline