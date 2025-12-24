from pathlib import Path

import pytest


@pytest.fixture
def sample_file(tmp_path: Path) -> Path:
    f = tmp_path / "sample.txt"
    f.write_text("test content")
    return f


@pytest.fixture
def empty_file(tmp_path: Path) -> Path:
    f = tmp_path / "empty.txt"
    f.write_text("")
    return f
