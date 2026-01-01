"""Items subcommands: {project} items list|add|remove

Example of modular CLI using Typer's add_typer() pattern.
Each command group lives in its own file under commands/.
"""

from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from .. import TYPER_SETTINGS

app = typer.Typer(help="Manage items", context_settings=TYPER_SETTINGS)
console = Console()


@app.command()
def list(
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help="Show details")] = False,
):
    """List all items."""
    table = Table(title="Items")
    table.add_column("ID", style="cyan")
    table.add_column("Name")
    if verbose:
        table.add_column("Details")

    # Example data - replace with actual logic
    table.add_row("1", "Example item", "Details here" if verbose else None)

    console.print(table)


@app.command()
def add(
    name: Annotated[str, typer.Argument(help="Item name")],
):
    """Add a new item."""
    console.print(f"[green]Added:[/green] {name}")


@app.command()
def remove(
    item_id: Annotated[str, typer.Argument(help="Item ID to remove")],
    force: Annotated[bool, typer.Option("--force", "-f", help="Skip confirmation")] = False,
):
    """Remove an item."""
    if not force:
        confirm = typer.confirm(f"Remove item {item_id}?")
        if not confirm:
            raise typer.Abort()

    console.print(f"[red]Removed:[/red] {item_id}")
