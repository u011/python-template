from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from .core import process_file
from .models import Config

app = typer.Typer(help="{PROJECT} CLI", no_args_is_help=True)
console = Console()


@app.command()
def run(
    path: Annotated[Path, typer.Argument(help="File to process")],
    output: Annotated[Path | None, typer.Option("--output", "-o", help="Output file")] = None,
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help="Verbose output")] = False,
):
    """Process a file."""
    config = Config(verbose=verbose)
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


if __name__ == "__main__":
    app()
