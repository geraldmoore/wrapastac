default:
    @just --list

# Run all checks
check: lint typecheck test

# Run ruff linter
lint:
    uv run ruff check .

# Run ruff formatter check (without fixes)
format-check:
    uv run ruff format --check .

# Format code with ruff (applies fixes)
format:
    uv run ruff format .
    uv run ruff check --fix .

# Run ty type checker
typecheck:
    uv run ty check

# Install prek git hooks
prek-install:
    uvx prek install
    
# Run all prek hooks
prek:
    uvx prek run --all-files

# Run tests
test *args:
    uv run pytest {{ args }}

# Run tests with coverage
test-cov:
    uv run pytest --cov=src/wrapastac --cov-report=term-missing

# Install dependencies and prek hooks
install:
    uv sync
    uvx prek install
