# Project Initialization Guide

## Create New Project from Template

### 1. Copy Template

```bash
# Replace 'myproject' with your project name (lowercase, hyphens ok)
PROJECT=myproject

# Copy template
cp -r /path/to/template ~/dev/$PROJECT
cd ~/dev/$PROJECT

# Rename {project} directories and files
mv src/{project} src/$PROJECT
```

### 2. Replace Placeholders

Replace in all files:
- `{project}` → `myproject` (lowercase, underscores for Python package)
- `{PROJECT}` → `MyProject` (display name, title case)

```bash
# macOS/BSD sed
fd -t f | xargs sed -i '' "s/{project}/$PROJECT/g"
fd -t f | xargs sed -i '' "s/{PROJECT}/MyProject/g"

# Linux sed
fd -t f | xargs sed -i "s/{project}/$PROJECT/g"
fd -t f | xargs sed -i "s/{PROJECT}/MyProject/g"
```

### 3. Initialize Environment

```bash
# Create virtual environment and install deps
uv sync

# Verify installation
uv run $PROJECT --help
uv run pytest
```

### 4. Initialize Git

```bash
git init
git add .
git commit -m "Initial commit from template"
```

### 5. Update Project Metadata

Edit `pyproject.toml`:
- `description`: One-line project description
- `dependencies`: Add/remove as needed

Edit `CLAUDE.md`:
- Update description and project-specific instructions

## Project Structure Conventions

```
myproject/
├── CLAUDE.md           # AI agent instructions
├── pyproject.toml      # Project config
├── uv.lock             # Lock file (commit this)
├── .gitignore
├── src/
│   └── myproject/
│       ├── __init__.py # Version only
│       ├── cli.py      # CLI entry point
│       ├── core.py     # Business logic
│       └── models.py   # Pydantic models
└── tests/
    ├── conftest.py     # Shared fixtures
    └── test_core.py    # Core tests
```

## File Responsibilities

| File | Purpose | When to Add |
|------|---------|-------------|
| `cli.py` | Typer commands, console output | Always exists |
| `core.py` | Main logic, algorithms | Always exists |
| `models.py` | Pydantic models, data structures | Always exists |
| `config.py` | Config loading (TOML, env) | When app needs config file |
| `api.py` | HTTP client, external services | When calling APIs |
| `db.py` | Database operations | When using database |

## Adding New Files

When core.py exceeds ~200-300 lines, split by domain:

```
src/myproject/
├── cli.py
├── models.py
├── fetch.py      # fetching logic
├── parse.py      # parsing logic
└── export.py     # export logic
```

## Dependency Management

```bash
# Add runtime dependency
uv add httpx

# Add dev dependency
uv add --group dev pytest-asyncio

# Remove dependency
uv remove httpx

# Update all
uv lock --upgrade
uv sync
```

## Common pyproject.toml Patterns

### Entry Points

```toml
[project.scripts]
myproject = "myproject.cli:app"        # Main CLI
mp = "myproject.cli:app"               # Short alias
```

### Optional Dependencies

```toml
[project.optional-dependencies]
api = ["fastapi>=0.100", "uvicorn>=0.23"]
```

### Ruff Rules

```toml
[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "F",    # pyflakes
    "I",    # isort
    "UP",   # pyupgrade
    "B",    # flake8-bugbear
    "SIM",  # flake8-simplify
]
ignore = [
    "E501",  # line too long (handled by formatter)
]
```

## Git Workflow

```bash
# Feature branch
git checkout -b feat/feature-name

# Commit format
git commit -m "Add feature description"
git commit -m "Fix bug description"
git commit -m "Refactor module description"

# Before PR
uv run ruff check . --fix
uv run ruff format .
uv run pytest
```
