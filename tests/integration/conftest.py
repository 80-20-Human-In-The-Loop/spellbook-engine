"""Integration test fixtures and utilities."""

import re
from collections.abc import Callable
from pathlib import Path

import pytest

from spellbook_engine import SpellBlockRegistry, SpellbookParser


@pytest.fixture
def parser_with_builtins() -> SpellbookParser:
    """Create a parser instance with built-in SpellBlocks loaded."""
    registry = SpellBlockRegistry(load_builtins=True)
    return SpellbookParser(registry=registry)


@pytest.fixture
def parser_without_builtins() -> SpellbookParser:
    """Create a parser instance without built-in SpellBlocks."""
    registry = SpellBlockRegistry(load_builtins=False)
    return SpellbookParser(registry=registry)


def normalize_html(html: str) -> str:
    """
    Normalize HTML for comparison.

    - Strips leading/trailing whitespace
    - Normalizes multiple spaces to single space
    - Normalizes newlines
    - Removes whitespace around tags
    """
    # Remove leading/trailing whitespace from each line
    lines = [line.strip() for line in html.splitlines()]

    # Join lines and normalize whitespace
    normalized = " ".join(lines)

    # Normalize multiple spaces to single space
    normalized = re.sub(r"\s+", " ", normalized)

    # Normalize whitespace around tags
    normalized = re.sub(r">\s+<", "><", normalized)

    return normalized.strip()


def compare_html(actual: str, expected: str, normalize: bool = True) -> bool:
    """
    Compare two HTML strings.

    Args:
        actual: The actual HTML output
        expected: The expected HTML output
        normalize: Whether to normalize before comparison (default True)

    Returns:
        True if HTML matches, False otherwise
    """
    if normalize:
        return normalize_html(actual) == normalize_html(expected)
    return actual == expected


@pytest.fixture
def html_comparator() -> Callable[[str, str, bool], bool]:
    """Return the compare_html function as a fixture."""
    return compare_html


@pytest.fixture
def html_normalizer() -> Callable[[str], str]:
    """Return the normalize_html function as a fixture."""
    return normalize_html


def load_dummy_file(filename: str, dummy_files_dir: Path) -> str:
    """Load content from a dummy file."""
    file_path = dummy_files_dir / filename
    if not file_path.exists():
        raise FileNotFoundError(f"Dummy file not found: {file_path}")
    return file_path.read_text()


def load_golden_file(filename: str, golden_files_dir: Path) -> str | None:
    """Load content from a golden file, return None if doesn't exist."""
    file_path = golden_files_dir / filename
    if not file_path.exists():
        return None
    return file_path.read_text()


def save_golden_file(filename: str, content: str, golden_files_dir: Path) -> None:
    """Save content to a golden file."""
    file_path = golden_files_dir / filename
    file_path.write_text(content)


@pytest.fixture
def dummy_loader(dummy_files_dir: Path) -> Callable[[str], str]:
    """Fixture to load dummy files."""

    def _load(filename: str) -> str:
        return load_dummy_file(filename, dummy_files_dir)

    return _load


@pytest.fixture
def golden_loader(golden_files_dir: Path) -> Callable[[str], str | None]:
    """Fixture to load golden files."""

    def _load(filename: str) -> str | None:
        return load_golden_file(filename, golden_files_dir)

    return _load


@pytest.fixture
def golden_saver(golden_files_dir: Path, update_golden_files: bool) -> Callable[[str, str], None]:
    """Fixture to save golden files (only if update flag is set)."""

    def _save(filename: str, content: str) -> None:
        if update_golden_files:
            save_golden_file(filename, content, golden_files_dir)

    return _save
