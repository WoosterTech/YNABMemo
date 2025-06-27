# Makefile for YNABMemo - uv-managed CLI tool

# Variables
PYTHON_VERSION := 3.12
PACKAGE_NAME := ynabmemo
CLI_NAME := yna
CLI_FILE := ynabmemo.cli.cli
SRC_DIR := src
TEST_DIR := tests
BUILD_DIR := dist
DOCS_DIR := docs

# Colors for terminal output
GREEN := \033[0;32m
YELLOW := \033[1;33m
RED := \033[0;31m
NC := \033[0m # No Color

.PHONY: help install install-dev sync clean test test-cov lint format type-check \
        pre-commit build publish docs cli-docs run dev-install clean-build \
        clean-pyc clean-test clean-all check-deps security-check tox

# Default target
help: ## Show this help message
	@echo "YNABMemo - uv-managed CLI tool"
	@echo ""
	@echo "Available targets:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Installation targets
install: ## Install the package in production mode
	@echo "$(YELLOW)Installing package...$(NC)"
	uv sync --no-dev
	@echo "$(GREEN)Installation complete!$(NC)"

install-dev: ## Install the package with development dependencies
	@echo "$(YELLOW)Installing package with dev dependencies...$(NC)"
	uv sync --all-groups
	@echo "$(GREEN)Development installation complete!$(NC)"

sync: ## Sync dependencies with lockfile
	@echo "$(YELLOW)Syncing dependencies...$(NC)"
	uv sync --all-groups
	@echo "$(GREEN)Dependencies synced!$(NC)"

dev-install: install-dev pre-commit-install ## Install dev dependencies and setup pre-commit hooks

# Development targets
run: ## Run the CLI tool (use ARGS="your args" to pass arguments)
	@echo "$(YELLOW)Running $(CLI_NAME)...$(NC)"
	uv run python -m $(PACKAGE_NAME).cli.cli $(ARGS)

# Testing targets
test: ## Run tests
	@echo "$(YELLOW)Running tests...$(NC)"
	uv run pytest $(TEST_DIR) -v

test-cov: ## Run tests with coverage
	@echo "$(YELLOW)Running tests with coverage...$(NC)"
	uv run pytest $(TEST_DIR) --cov=$(SRC_DIR)/$(PACKAGE_NAME) --cov-report=html --cov-report=term-missing -v

test-watch: ## Run tests in watch mode
	@echo "$(YELLOW)Running tests in watch mode...$(NC)"
	uv run pytest-watch $(TEST_DIR) -v

# Code quality targets
lint: ## Run linting with ruff
	@echo "$(YELLOW)Running linter...$(NC)"
	uv run ruff check $(SRC_DIR) $(TEST_DIR)

format: ## Format code with ruff
	@echo "$(YELLOW)Formatting code...$(NC)"
	uv run ruff format $(SRC_DIR) $(TEST_DIR)

format-check: ## Check code formatting without making changes
	@echo "$(YELLOW)Checking code formatting...$(NC)"
	uv run ruff format --check $(SRC_DIR) $(TEST_DIR)

type-check: ## Run type checking with basedpyright
	@echo "$(YELLOW)Running type checker...$(NC)"
	uv run basedpyright $(SRC_DIR) $(TEST_DIR)

# Pre-commit targets
pre-commit: ## Run pre-commit hooks on all files
	@echo "$(YELLOW)Running pre-commit hooks...$(NC)"
	uv run pre-commit run --all-files

pre-commit-install: ## Install pre-commit hooks
	@echo "$(YELLOW)Installing pre-commit hooks...$(NC)"
	uv run pre-commit install

# Quality check target combining all checks
check: lint format-check type-check test ## Run all quality checks

# Security and dependency checking
security-check: ## Run security checks
	@echo "$(YELLOW)Running security checks...$(NC)"
	uv run pip-audit

check-deps: ## Check for dependency issues
	@echo "$(YELLOW)Checking dependencies...$(NC)"
	uv run deptry .

# Build targets
build: clean-build ## Build the package
	@echo "$(YELLOW)Building package...$(NC)"
	uv build
	@echo "$(GREEN)Build complete! Artifacts in $(BUILD_DIR)/$(NC)"

build-wheel: clean-build ## Build wheel only
	@echo "$(YELLOW)Building wheel...$(NC)"
	uv build --wheel

build-sdist: clean-build ## Build source distribution only
	@echo "$(YELLOW)Building source distribution...$(NC)"
	uv build --sdist

# Documentation targets
docs: ## Generate project documentation
	@echo "$(YELLOW)Generating documentation...$(NC)"
	@mkdir -p $(DOCS_DIR)
	@echo "$(GREEN)Documentation generated!$(NC)"

cli-docs: ## Generate CLI documentation
	@echo "$(YELLOW)Generating CLI documentation...$(NC)"
	./scripts/build_cli_docs.sh
	@echo "$(GREEN)CLI documentation generated as CLI_README.md!$(NC)"

# Tox targets
tox: ## Run tox tests across multiple Python versions
	@echo "$(YELLOW)Running tox...$(NC)"
	uv run tox

tox-recreate: ## Recreate tox environments
	@echo "$(YELLOW)Recreating tox environments...$(NC)"
	uv run tox -r

# Publishing targets
publish-test: build ## Publish to Test PyPI
	@echo "$(YELLOW)Publishing to Test PyPI...$(NC)"
	uv publish --repository testpypi

publish: build ## Publish to PyPI
	@echo "$(YELLOW)Publishing to PyPI...$(NC)"
	uv publish

# Cleaning targets
clean-build: ## Remove build artifacts
	@echo "$(YELLOW)Cleaning build artifacts...$(NC)"
	rm -rf $(BUILD_DIR)/
	rm -rf *.egg-info/
	rm -rf build/

clean-pyc: ## Remove Python file artifacts
	@echo "$(YELLOW)Cleaning Python artifacts...$(NC)"
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +

clean-test: ## Remove test and coverage artifacts
	@echo "$(YELLOW)Cleaning test artifacts...$(NC)"
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf coverage.xml
	rm -rf .tox/

clean-all: clean-build clean-pyc clean-test ## Remove all artifacts
	@echo "$(YELLOW)Cleaning all artifacts...$(NC)"
	rm -rf .ruff_cache/
	rm -rf .mypy_cache/
	rm -rf .basedpyright_cache/
	@echo "$(GREEN)All artifacts cleaned!$(NC)"

clean: clean-all ## Alias for clean-all

# Development workflow targets
dev-setup: install-dev pre-commit-install ## Setup development environment
	@echo "$(GREEN)Development environment setup complete!$(NC)"

dev-check: format lint type-check test ## Run development checks
	@echo "$(GREEN)All development checks passed!$(NC)"

# Version management (requires commitizen)
version-bump: ## Bump version and create changelog
	@echo "$(YELLOW)Bumping version...$(NC)"
	uv run cz bump --changelog

version-check: ## Check current version
	@echo "$(YELLOW)Current version:$(NC)"
	uv run python -c "from importlib.metadata import version; print(version('$(PACKAGE_NAME)'))"

# Environment info
env-info: ## Show environment information
	@echo "$(YELLOW)Environment Information:$(NC)"
	@echo "Python version: $(shell python --version)"
	@echo "UV version: $(shell uv --version)"
	@echo "Current directory: $(shell pwd)"
	@echo "Package name: $(PACKAGE_NAME)"
	@echo "CLI name: $(CLI_NAME)"

# Quick development commands
quick-test: ## Run a quick subset of tests
	@echo "$(YELLOW)Running quick tests...$(NC)"
	uv run pytest $(TEST_DIR) -x --tb=short

quick-check: format-check lint ## Run quick quality checks
	@echo "$(GREEN)Quick checks complete!$(NC)"

# Debug targets
debug-deps: ## Show dependency tree
	@echo "$(YELLOW)Dependency tree:$(NC)"
	uv tree

debug-env: ## Show current environment
	@echo "$(YELLOW)Current environment:$(NC)"
	uv pip list
