# {PROJECT} Project

## Quick Start

```bash
uv sync                              # install deps
uv run {project} --help              # run CLI
uv run pytest                        # test
uv run ruff check src tests          # lint
uv run ruff format src tests         # format
```

## Project Structure

```
{project}/
├── CLAUDE.md           # agent instructions (this file)
├── pyproject.toml      # project config, deps, tools
├── uv.lock             # lockfile (committed)
├── src/
│   └── {project}/
│       ├── __init__.py # version only
│       ├── cli.py      # typer app, entry point
│       ├── core.py     # business logic
│       └── models.py   # pydantic models
└── tests/
    ├── conftest.py     # shared fixtures
    └── test_core.py
```

## Code Rules

### Type Hints (Required)
- All function signatures typed
- Modern syntax: `list[str]`, `dict[str, int]`, `str | None`
- CLI args: `Annotated[type, typer.Option(...)]`

### Naming
- Descriptive: `fetch_user_by_email()` not `get_u()`
- No abbreviations unless universal (url, id, http)

### Imports
- stdlib, then third-party, then local (ruff handles)
- Absolute imports from package root

### Files
- Split at ~200-300 lines
- One class/concern per file
- No `utils.py` dumping grounds

### Paths
- Always `pathlib.Path`, never `os.path`

### Data
- Pydantic `BaseModel` for all structured data
- `Field(default_factory=list)` for mutable defaults

### CLI (typer)
- `no_args_is_help=True` on app
- Rich console for output
- Annotated args with help text

## Patterns

### CLI Entry Point
```python
from typing import Annotated
import typer
from rich.console import Console

app = typer.Typer(help="{PROJECT} CLI", no_args_is_help=True)
console = Console()

@app.command()
def cmd(
    path: Annotated[Path, typer.Argument(help="File to process")],
    output: Annotated[Path | None, typer.Option("--output", "-o")] = None,
    verbose: Annotated[bool, typer.Option("--verbose", "-v")] = False,
):
    """Command description."""
    console.print(f"[green]Processing:[/green] {path}")
```

### Pydantic Model
```python
from pydantic import BaseModel, Field

class Config(BaseModel):
    timeout: int = 30
    tags: list[str] = Field(default_factory=list)
```

### Testing
```python
import pytest

@pytest.mark.parametrize("input,expected", [
    ("a", 1),
    ("b", 2),
])
def test_func(input, expected):
    assert func(input) == expected
```

## Commands Reference

```bash
# Package management
uv add httpx                     # add dependency
uv add --group dev pytest        # add dev dep
uv sync                          # sync environment

# Development
uv run {project}                 # run CLI
uv run pytest -v                 # verbose tests
uv run pytest -k "test_name"     # specific test
uv run pytest --cov={project}    # coverage

# Code quality
uv run ruff check . --fix        # lint + autofix
uv run ruff format .             # format
```

## Don't

- Create abstractions until needed
- Write docstrings for obvious functions
- Add `utils.py` or `helpers.py`
- Over-engineer with layers/ports/adapters
- Add "just in case" flexibility
- Use `os.path` (use pathlib)
- Skip type hints
