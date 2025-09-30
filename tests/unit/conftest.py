"""Shared pytest fixtures for unit tests."""

from pathlib import Path

import pytest
from jinja2 import Template


@pytest.fixture
def mock_template() -> Template:
    """Create a simple mock Jinja2 template for testing."""
    template_string = "<div class='test'>{{ content }}</div>"
    return Template(template_string)


@pytest.fixture
def mock_template_with_vars() -> Template:
    """Create a template that uses multiple variables."""
    template_string = """
    <div class="{{ css_class }}" id="{{ element_id }}">
        <h3>{{ title }}</h3>
        <p>{{ content }}</p>
    </div>
    """
    return Template(template_string)


@pytest.fixture
def temp_spellblocks_dir(tmp_path: Path) -> Path:
    """Create a temporary directory for SpellBlock testing."""
    spellblocks_dir = tmp_path / "spellblocks"
    spellblocks_dir.mkdir()
    return spellblocks_dir


@pytest.fixture
def standard_structure_dir(temp_spellblocks_dir: Path) -> Path:
    """Create standard structure (templates/ and logic/ folders)."""
    templates_dir = temp_spellblocks_dir / "templates"
    logic_dir = temp_spellblocks_dir / "logic"
    templates_dir.mkdir()
    logic_dir.mkdir()

    # Create a simple test block
    template_content = "<div class='test-block'>{{ content }}</div>"
    (templates_dir / "testblock.html").write_text(template_content)

    logic_content = """
from spellbook_engine import BaseSpellBlock

class TestblockBlock(BaseSpellBlock):
    def get_context(self):
        return {"content": self.process_content()}
"""
    (logic_dir / "testblock.py").write_text(logic_content)

    return temp_spellblocks_dir


@pytest.fixture
def flat_structure_dir(temp_spellblocks_dir: Path) -> Path:
    """Create flat structure (.html and .py in same directory)."""
    # Create a simple test block
    template_content = "<div class='flat-block'>{{ content }}</div>"
    (temp_spellblocks_dir / "flatblock.html").write_text(template_content)

    logic_content = """
from spellbook_engine import BaseSpellBlock

class FlatblockBlock(BaseSpellBlock):
    def get_context(self):
        return {"content": self.process_content()}
"""
    (temp_spellblocks_dir / "flatblock.py").write_text(logic_content)

    return temp_spellblocks_dir
