.PHONY: help install lint lint-fix format type-check test test-cov qa clean

# Default target
help:
	@echo "Available targets:"
	@echo "  install     - Install dependencies"
	@echo "  lint        - Run ruff linter"
	@echo "  lint-fix    - Run ruff linter with auto-fix"
	@echo "  format      - Run ruff formatter"
	@echo "  type-check  - Run mypy type checker"
	@echo "  test        - Run pytest tests"
	@echo "  test-cov    - Run pytest tests with coverage"
	@echo "  qa          - Run all QA checks (lint + type-check + test)"
	@echo "  clean       - Clean build artifacts and cache"

# Install dependencies
install:
	uv sync

# Run ruff linter
lint:
	uv run ruff check .

# Run ruff linter with auto-fix
lint-fix:
	uv run ruff check . --fix

# Run ruff formatter
format:
	uv run ruff format .

# Run mypy type checker
type-check:
	uv run mypy .

# Run pytest tests
test:
	uv run pytest

# Run pytest tests with coverage
test-cov:
	uv run pytest --cov=app --cov-report=term-missing --cov-report=html

# Run all QA checks
qa: lint type-check test

# Clean build artifacts and cache
clean:
	rm -rf __pycache__
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf htmlcov
	rm -rf .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
