from pathlib import Path

from .models import Config


def process_file(path: Path, config: Config) -> str:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    content = path.read_text()

    if config.verbose:
        print(f"Processing {path} ({len(content)} bytes)")

    return content
