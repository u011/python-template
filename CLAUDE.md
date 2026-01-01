# {PROJECT} Project

## Quick Start

```bash
uv sync                              # install deps
uv run {project} --help              # run CLI
uv run pytest                        # test
uv run ruff check src tests          # lint
uv run ruff format src tests         # format
```

## Shell Wrapper (optional)

Skip typing `uv run` every time by creating a symlink:

```bash
# Option 1: Symlink to ~/.local/bin (add to PATH if needed)
ln -s "$(pwd)/bin/run" ~/.local/bin/{project}

# Option 2: Add project bin/ to PATH in shell config
# fish: fish_add_path (pwd)/bin
# bash: export PATH="$(pwd)/bin:$PATH"

# Now run directly
{project} --help
```

The `bin/run` wrapper auto-detects the project root and runs via `uv run`.

## Project Structure

```
{project}/
├── CLAUDE.md           # agent instructions (this file)
├── pyproject.toml      # project config, deps, tools
├── uv.lock             # lockfile (committed)
├── bin/
│   └── run             # shell wrapper (symlink to PATH)
├── config/
│   ├── default.toml    # default settings (versioned)
│   └── local.toml      # local overrides (gitignored)
├── src/
│   └── {project}/
│       ├── __init__.py # version + TYPER_SETTINGS
│       ├── cli.py      # main typer app, mounts subcommands
│       ├── config.py   # config loading from config/
│       ├── core.py     # business logic
│       ├── models.py   # pydantic models
│       ├── shell.py    # shell command utilities (sh library)
│       └── commands/   # subcommand modules (modular CLI)
│           ├── __init__.py
│           └── items.py    # example: {project} items list|add
└── tests/
    ├── conftest.py     # shared fixtures
    └── test_core.py
```

## Configuration

Configuration lives in `config/` (inside the repo, not `~/.config`):

```bash
config/
├── default.toml    # versioned defaults (committed)
└── local.toml      # local overrides (gitignored)
```

**Priority** (highest to lowest):
1. CLI arguments (`--verbose`, etc.)
2. Environment variables (`{PROJECT}_VERBOSE=1`)
3. `config/local.toml` (local overrides)
4. `config/default.toml` (defaults)

**Commands:**
```bash
{project} config              # show current config
cp config/default.toml config/local.toml  # create local overrides
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
- Keep under 400 LOC (agent-friendly context windows)
- Split at ~200-300 lines when practical
- One class/concern per file
- No `utils.py` dumping grounds

### Paths
- Always `pathlib.Path`, never `os.path`

### Data
- Pydantic `BaseModel` for all structured data
- `Field(default_factory=list)` for mutable defaults

### CLI (typer)
- `no_args_is_help=True` on main app
- `context_settings=TYPER_SETTINGS` on all Typer() instances (import from package root)
- Rich console for output
- Annotated args with help text

## Patterns

### CLI Entry Point
```python
from typing import Annotated
import typer
from rich.console import Console

from . import TYPER_SETTINGS
from .commands import items

app = typer.Typer(
    help="{PROJECT} CLI",
    no_args_is_help=True,
    context_settings=TYPER_SETTINGS,
)
console = Console()

# Mount subcommand groups
app.add_typer(items.app, name="items")  # → {project} items list|add|remove

@app.command()
def cmd(
    path: Annotated[Path, typer.Argument(help="File to process")],
    output: Annotated[Path | None, typer.Option("--output", "-o")] = None,
    verbose: Annotated[bool, typer.Option("--verbose", "-v")] = False,
):
    """Command description."""
    console.print(f"[green]Processing:[/green] {path}")
```

### Modular CLI (subcommands)
```python
# commands/items.py - each group in its own file
import typer
from rich.console import Console

from .. import TYPER_SETTINGS

app = typer.Typer(help="Manage items", context_settings=TYPER_SETTINGS)
console = Console()

@app.command()
def list():
    """List all items."""
    console.print("Items: ...")

@app.command()
def add(name: str):
    """Add an item."""
    console.print(f"[green]Added:[/green] {name}")
```

Usage: `{project} items list`, `{project} items add foo`

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

### Shell Commands (sh library)
```python
from {project}.shell import rm, rg, fd, run, sh

# Safe delete using rip (sends to trash)
rm("unwanted_file.txt")
rm("-rf", "old_directory/")

# Search with ripgrep - use rg directly, don't rename
for match in rg("TODO", "src/", _iter=True):
    print(match.strip())

# Find files with fd - use fd directly, don't rename
python_files = fd("-e", "py", "-t", "f")

# Stream output line by line
for line in rg("pattern", ".", _iter=True, _ok_code=[0, 1]):
    process(line)

# Any command via run() or sh
run("git", "status", "--short")
sh.docker.ps("-a")
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
- Use `subprocess` directly (use `shell.py` with sh library)
- Rename `rg`/`fd` to grep/find (keep modern names)
