# WrapASTAC

A Python SDK to wrap STAC satellite endpoints.

## Installation

```bash
pip install -e .
```

With [`uv`](https://docs.astral.sh/uv/):

```bash
uv sync
```

## Development

This project uses [`just`](https://github.com/casey/just) as a command runner. Run `just` to see all 
available commands:

```bash
just               # list available commands
just check         # run all checks (lint, typecheck, test)
just format        # Format code with ruff (applies fixes)
just format-check  # Run ruff formatter check (without fixes)
just install       # Install dependencies and prek hooks
just lint          # Run ruff linter
just prek          # Run all prek hooks
just prek-install  # Install prek git hooks
just test *args    # Run tests
just test-cov      # Run tests with coverage
just typecheck     # Run ty type checker
```

The project also uses [`prek`](https://prek.j178.dev/) for pre-commit hook management. These hooks 
automatically apply format and type checks on `git` commits only (not on the entire codebase). This 
ensures all committed code follows pre-defined standards, whilst the rest of the codebase can maintain
development flexibility. 

If you prefer to keep everything up to standard, use `just check` or the individual `just format` or 
`just lint` commands to run on the entire codebase.
