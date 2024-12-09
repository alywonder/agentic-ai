# Copyright 2024 Weavers @ Eternal Loom. All rights reserved.
# Use of this software is governed by the license that can be
# found in LICENSE file in the source repository.

# Default goal
default: all

# Check that uv is installed
uv:
    @uv --version || echo 'Please install uv: https://docs.astral.sh/uv/getting-started/installation/'

# Check that pre-commit is installed
pre-commit:
    @pre-commit -V || echo 'Please install pre-commit: https://pre-commit.com/'

# Install the package, dependencies, and pre-commit for local development
install: uv pre-commit
    uv sync --frozen --all-extras --all-packages --group lint --group docs
    pre-commit install --install-hooks

# Update local packages and uv.lock
sync: uv
    uv sync --all-extras --all-packages --group lint --group docs

# Format the code
format:
    uv run ruff format
    uv run ruff check --fix --fix-only

# Lint the code
lint:
    uv run ruff format --check
    uv run ruff check

# Run static type checking with Pyright
typecheck-pyright:
    uv run pyright

# Run static type checking with Mypy
typecheck-mypy:
    uv run mypy

# Run static type checking
typecheck: typecheck-pyright

# Run static type checking with both Pyright and Mypy
typecheck-all: typecheck-pyright typecheck-mypy

# Run tests and collect coverage data
test:
    uv run coverage run -m pytest
    @uv run coverage report

# Run tests on Python 3.9 to 3.13
test-all:
    UV_PROJECT_ENVIRONMENT=.venv310 uv run --python 3.10 --all-extras coverage run -p -m pytest
    UV_PROJECT_ENVIRONMENT=.venv311 uv run --python 3.11 --all-extras coverage run -p -m pytest
    UV_PROJECT_ENVIRONMENT=.venv312 uv run --python 3.12 --all-extras coverage run -p -m pytest
    UV_PROJECT_ENVIRONMENT=.venv313 uv run --python 3.13 --all-extras coverage run -p -m pytest
    @uv run coverage combine
    @uv run coverage report

# Run tests and generate a coverage report
testcov: test
    @echo "building coverage html"
    @uv run coverage html

# Build the documentation
docs:
    uv run mkdocs build --no-strict

# Build and serve the documentation
docs-serve:
    uv run mkdocs serve --no-strict

# Run all default tasks
all: format lint typecheck testcov
