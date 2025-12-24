# Code Standards for AI Agents

This document defines code quality expectations for AI agents working on this codebase.

## Format Expectations

### Before Submitting Code

1. **Run formatters**: `uv run ruff format .`
2. **Run linters**: `uv run ruff check . --fix`
3. **Run tests**: `uv run pytest`
4. **Verify CLI**: `uv run {project} --help`

### Type Hints

**Required on all function signatures.**

```python
# GOOD
def fetch_user(user_id: str, timeout: int = 30) -> User | None:
    ...

def process_items(items: list[Item], config: Config) -> dict[str, Result]:
    ...

# BAD - missing types
def fetch_user(user_id, timeout=30):
    ...
```

### Modern Syntax

Use Python 3.11+ type syntax:

```python
# GOOD
list[str]           # not List[str]
dict[str, int]      # not Dict[str, int]
str | None          # not Optional[str]
tuple[int, ...]     # not Tuple[int, ...]

# BAD - old syntax
from typing import List, Dict, Optional, Tuple
```

### CLI Arguments

Use Annotated with full metadata:

```python
# GOOD
def cmd(
    path: Annotated[Path, typer.Argument(help="File to process")],
    output: Annotated[Path | None, typer.Option("--output", "-o", help="Output file")] = None,
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help="Verbose output")] = False,
):

# BAD - missing help text
def cmd(path: Path, output: Path = None, verbose: bool = False):
```

### Pydantic Models

```python
# GOOD
class Config(BaseModel):
    timeout: int = 30
    tags: list[str] = Field(default_factory=list)  # mutable default

# BAD - mutable default
class Config(BaseModel):
    tags: list[str] = []  # Will cause issues
```

## Code Organization

### Import Order

Ruff handles this, but understand the pattern:
1. Standard library
2. Third-party packages
3. Local imports

```python
import json
from pathlib import Path

import httpx
from pydantic import BaseModel

from .models import Config
from .core import process
```

### File Size

Split files at ~200-300 lines. Signs you need to split:
- Multiple unrelated classes
- Imports getting long
- Hard to find functions

### Function Size

If a function exceeds ~50 lines, consider splitting.

## What NOT to Do

### Over-Engineering

```python
# BAD - unnecessary abstraction
class FileProcessorFactory:
    def create_processor(self, type: str) -> BaseProcessor:
        ...

# GOOD - just do it
def process_file(path: Path) -> str:
    return path.read_text()
```

### Premature Generalization

```python
# BAD - config for everything
def fetch(url: str, method: str = "GET", headers: dict = None,
          auth: tuple = None, timeout: int = 30, retries: int = 3,
          backoff: float = 1.5, verify_ssl: bool = True):

# GOOD - simple defaults, extend when needed
def fetch(url: str, timeout: int = 30) -> Response:
```

### Docstrings for Obvious Code

```python
# BAD - obvious docstring
def get_user_by_id(user_id: str) -> User:
    """Get a user by their ID.

    Args:
        user_id: The ID of the user to get.

    Returns:
        The user with the given ID.
    """
    return db.users.get(user_id)

# GOOD - code speaks for itself
def get_user_by_id(user_id: str) -> User:
    return db.users.get(user_id)
```

### Comments for Clear Code

```python
# BAD - comment restates code
# Increment counter by 1
counter += 1

# GOOD - comment explains WHY (when not obvious)
# Skip first byte: BOM marker in Windows-generated files
content = data[1:]
```

### Utils Dumping Ground

```python
# BAD
# utils.py with 50 unrelated functions

# GOOD - domain-specific modules
# format.py - formatting functions
# validate.py - validation functions
```

## Testing Standards

### Test Naming

```python
# GOOD - describes behavior
def test_process_file_returns_content():
def test_process_file_raises_on_missing_file():
def test_fetch_retries_on_timeout():

# BAD - vague
def test_process():
def test_error():
```

### Use Fixtures

```python
# GOOD
@pytest.fixture
def sample_config() -> Config:
    return Config(timeout=10)

def test_something(sample_config):
    result = process(sample_config)

# BAD - repeated setup
def test_something():
    config = Config(timeout=10)
    result = process(config)
```

### Parametrize When Appropriate

```python
# GOOD - test multiple cases
@pytest.mark.parametrize("input,expected", [
    ("valid", True),
    ("invalid", False),
    ("", False),
])
def test_validate(input, expected):
    assert validate(input) == expected

# BAD - separate tests for each case
def test_validate_valid():
    assert validate("valid") == True

def test_validate_invalid():
    assert validate("invalid") == False
```

## Error Handling

### Be Specific

```python
# GOOD
def load_config(path: Path) -> Config:
    if not path.exists():
        raise FileNotFoundError(f"Config not found: {path}")

    try:
        data = tomllib.loads(path.read_text())
    except tomllib.TOMLDecodeError as e:
        raise ValueError(f"Invalid TOML in {path}: {e}")

    return Config(**data)

# BAD - swallows errors
def load_config(path: Path) -> Config | None:
    try:
        return Config(**tomllib.loads(path.read_text()))
    except Exception:
        return None
```

### Don't Over-Handle

```python
# BAD - unnecessary handling
def add(a: int, b: int) -> int:
    try:
        return a + b
    except TypeError as e:
        raise TypeError(f"Cannot add {type(a)} and {type(b)}") from e

# GOOD - let it fail naturally
def add(a: int, b: int) -> int:
    return a + b
```

## Checklist Before Completion

- [ ] All functions have type hints
- [ ] Using modern Python 3.11+ syntax
- [ ] CLI commands have help text
- [ ] No unnecessary abstractions
- [ ] No docstrings for obvious functions
- [ ] Tests pass: `uv run pytest`
- [ ] Lints pass: `uv run ruff check .`
- [ ] Format clean: `uv run ruff format --check .`
