from pathlib import Path

import pytest

from {project}.core import process_file
from {project}.models import Config


def test_process_file(sample_file: Path):
    config = Config()
    result = process_file(sample_file, config)
    assert result == "test content"


def test_process_file_not_found(tmp_path: Path):
    config = Config()
    with pytest.raises(FileNotFoundError):
        process_file(tmp_path / "nonexistent.txt", config)


def test_process_file_verbose(sample_file: Path, capsys):
    config = Config(verbose=True)
    process_file(sample_file, config)
    captured = capsys.readouterr()
    assert "Processing" in captured.out
