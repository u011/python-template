"""Shell utilities using the sh library.

Provides Pythonic access to shell commands with safer defaults.

Usage:
    from {project}.shell import rm, rg, fd, run

    # Safe delete (uses rip, sends to trash)
    rm("unwanted_file.txt")
    rm("-rf", "old_directory/")

    # Fast search with ripgrep
    for line in rg("TODO", "src/", _iter=True):
        print(line)

    # Find files with fd
    for path in fd("-e", "py", _iter=True):
        print(path.strip())

    # Any command via run()
    run("git", "status", "--short")

    # Or access sh directly for any command
    from {project}.shell import sh
    sh.git.log("--oneline", "-5")
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import sh as _sh

if TYPE_CHECKING:
    from sh import Command

__all__ = [
    "sh",
    "rm",
    "rg",
    "fd",
    "run",
    "command",
]

# Re-export sh for direct access to any command
sh = _sh


def command(name: str) -> "Command":
    """Get a command by name, raising helpful error if not found."""
    try:
        return _sh.Command(name)
    except _sh.CommandNotFound:
        raise RuntimeError(
            f"Command '{name}' not found in PATH. "
            f"Install it or check your environment."
        ) from None


def run(cmd: str, *args: str, **kwargs) -> str:
    """Run any command by name with arguments.

    Args:
        cmd: Command name (looked up in PATH)
        *args: Command arguments
        **kwargs: Passed to sh (e.g., _iter=True, _bg=True)

    Returns:
        Command output as string (unless _iter=True)

    Example:
        run("git", "status", "--short")
        run("docker", "ps", "-a")
    """
    return command(cmd)(*args, **kwargs)


# Safe rm using rip (sends to trash instead of permanent delete)
# Install: cargo install rm-improved
try:
    rm: "Command" = _sh.rip
except _sh.CommandNotFound:
    # Fallback warning - don't silently use rm
    def rm(*args, **kwargs):
        raise RuntimeError(
            "rip not found. Install with: cargo install rm-improved\n"
            "Or use sh.rm directly if you want permanent deletion."
        )


# ripgrep - fast grep alternative
# Install: cargo install ripgrep (or: brew install ripgrep)
try:
    rg: "Command" = _sh.rg
except _sh.CommandNotFound:
    rg = None  # type: ignore


# fd - fast find alternative
# Install: cargo install fd-find (or: brew install fd)
try:
    fd: "Command" = _sh.fd
except _sh.CommandNotFound:
    fd = None  # type: ignore
