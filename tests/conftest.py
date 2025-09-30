"""Root-level shared pytest fixtures for all tests."""

import os
from pathlib import Path

import pytest


@pytest.fixture
def tests_dir() -> Path:
    """Get the tests directory path."""
    return Path(__file__).parent


@pytest.fixture
def dummy_files_dir(tests_dir: Path) -> Path:
    """Get the _dummy_files directory path."""
    return tests_dir / "_dummy_files"


@pytest.fixture
def golden_files_dir(tests_dir: Path) -> Path:
    """Get the _golden_files directory path."""
    return tests_dir / "_golden_files"


@pytest.fixture
def update_golden_files() -> bool:
    """Check if golden files should be updated."""
    return os.getenv("SPELLBOOK_UPDATE_GOLDEN", "").lower() in ("1", "true", "yes")


@pytest.fixture
def project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent
