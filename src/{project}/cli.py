from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from .commands import items
from .config import load_config
from .core import process_file

app = typer.Typer(help="{PROJECT} CLI", no_args_is_help=True)
console = Console()

# Mount subcommand groups (modular CLI pattern)
# Usage: {project} items list, {project} items add, etc.
app.add_typer(items.app, name="items")


@app.command()
def run(
    path: Annotated[Path, typer.Argument(help="File to process")],
    output: Annotated[Path | None, typer.Option("--output", "-o", help="Output file")] = None,
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help="Verbose output")] = False,
):
    """Process a file."""
    config = load_config(verbose=verbose if verbose else None)
    result = process_file(path, config)

    if output:
        output.write_text(result)
        console.print(f"[green]Written to:[/green] {output}")
    else:
        console.print(result)


@app.command()
def version():
    """Show version."""
    from . import __version__

    console.print(f"{__version__}")


@app.command(name="config")
def show_config():
    """Show current configuration."""
    from .config import get_config_dir, load_config

    config = load_config()
    config_dir = get_config_dir()

    console.print(f"[dim]Config dir:[/dim] {config_dir}")
    console.print(f"[dim]Default:[/dim]   {config_dir / 'default.toml'}")
    console.print(f"[dim]Local:[/dim]     {config_dir / 'local.toml'}")
    console.print()
    console.print("[bold]Current config:[/bold]")
    for key, value in config.model_dump().items():
        console.print(f"  {key}: {value}")


if __name__ == "__main__":
    app()
