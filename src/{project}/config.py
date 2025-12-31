"""Configuration loading from repo's config/ folder.

Priority (highest to lowest):
1. CLI arguments (handled in cli.py)
2. Environment variables ({PROJECT}_* prefix)
3. config/local.toml (gitignored, for local overrides)
4. config/default.toml (versioned defaults)
"""

import os
import tomllib
from pathlib import Path
from typing import Any

from .models import Config


def find_project_root() -> Path:
    """Find project root by looking for pyproject.toml or .git."""
    current = Path.cwd()
    for parent in [current, *current.parents]:
        if (parent / "pyproject.toml").exists() or (parent / ".git").exists():
            return parent
    return current


def get_config_dir() -> Path:
    """Get the config directory path (repo's config/ folder)."""
    return find_project_root() / "config"


def load_toml(path: Path) -> dict[str, Any]:
    """Load a TOML file, returning empty dict if not found."""
    if not path.exists():
        return {}
    with path.open("rb") as f:
        return tomllib.load(f)


def merge_dicts(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Deep merge override into base."""
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value
    return result


def load_config(**cli_overrides: Any) -> Config:
    """Load configuration with priority: CLI > env > local.toml > default.toml.

    Args:
        **cli_overrides: CLI argument overrides (e.g., verbose=True)

    Returns:
        Merged Config object
    """
    config_dir = get_config_dir()

    # Load defaults, then local overrides
    defaults = load_toml(config_dir / "default.toml")
    local = load_toml(config_dir / "local.toml")
    merged = merge_dicts(defaults, local)

    # Extract the 'general' section as flat config
    config_data = merged.get("general", {})

    # Apply environment variable overrides
    env_prefix = "{PROJECT}_".upper()
    for key in ["verbose", "timeout"]:
        env_key = f"{env_prefix}{key.upper()}"
        if env_key in os.environ:
            value = os.environ[env_key]
            if key == "verbose":
                config_data[key] = value.lower() in ("1", "true", "yes")
            elif key == "timeout":
                config_data[key] = int(value)

    # Apply CLI overrides (highest priority)
    for key, value in cli_overrides.items():
        if value is not None:
            config_data[key] = value

    return Config(**config_data)
