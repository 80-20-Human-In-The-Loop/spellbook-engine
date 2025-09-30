"""Unit tests for SpellBlockRegistry discovery system."""

from pathlib import Path
from typing import Any

import pytest

from spellbook_engine import BaseSpellBlock, SpellBlockRegistry
from spellbook_engine.exceptions import SpellBlockDiscoveryError, SpellBlockLoadError


class TestRegistryBasicInitialization:
    """Test basic SpellBlockRegistry initialization."""

    def test_init_with_defaults(self) -> None:
        """Test that registry can be initialized with defaults."""
        # Should load builtins without error
        registry = SpellBlockRegistry()
        assert registry is not None

    def test_init_loads_builtins(self) -> None:
        """Test that built-in SpellBlocks are loaded by default."""
        registry = SpellBlockRegistry()
        blocks = registry.list_blocks()

        # Should have built-in blocks
        assert len(blocks) > 0
        # Check for known builtins
        assert "alert" in blocks or "card" in blocks or "quote" in blocks

    def test_init_without_builtins(self) -> None:
        """Test initialization without loading built-ins."""
        registry = SpellBlockRegistry(load_builtins=False)
        blocks = registry.list_blocks()

        # Should have no blocks loaded
        assert len(blocks) == 0

    def test_list_blocks(self) -> None:
        """Test that list_blocks returns a list of block names."""
        registry = SpellBlockRegistry()
        blocks = registry.list_blocks()
        assert isinstance(blocks, list)
        for block_name in blocks:
            assert isinstance(block_name, str)


class TestRegistryStandardStructure:
    """Test discovery with standard directory structure."""

    def test_discover_standard_structure(self, standard_structure_dir: Path) -> None:
        """Test loading from standard structure (templates/ and logic/)."""
        registry = SpellBlockRegistry(source=standard_structure_dir, load_builtins=False)
        blocks = registry.list_blocks()
        assert "testblock" in blocks

    def test_get_block_class(self, standard_structure_dir: Path) -> None:
        """Test retrieving a block class from standard structure."""
        registry = SpellBlockRegistry(source=standard_structure_dir, load_builtins=False)
        block_class = registry.get_block("testblock")
        assert block_class is not None
        assert issubclass(block_class, BaseSpellBlock)

    def test_get_template(self, standard_structure_dir: Path) -> None:
        """Test retrieving a template from standard structure."""
        registry = SpellBlockRegistry(source=standard_structure_dir, load_builtins=False)
        template = registry.get_template("testblock")
        assert template is not None

    def test_create_block_instance(self, standard_structure_dir: Path) -> None:
        """Test creating a block instance from standard structure."""
        registry = SpellBlockRegistry(source=standard_structure_dir, load_builtins=False)
        block = registry.create_block("testblock", content="Test content")
        assert block is not None
        assert isinstance(block, BaseSpellBlock)
        assert block.content == "Test content"

    def test_render_block_from_registry(self, standard_structure_dir: Path) -> None:
        """Test rendering a block created from registry."""
        registry = SpellBlockRegistry(source=standard_structure_dir, load_builtins=False)
        block = registry.create_block("testblock", content="Hello World")
        assert block is not None
        html = block.render()
        assert "Hello World" in html
        assert "test-block" in html


class TestRegistryFlatStructure:
    """Test discovery with flat directory structure."""

    def test_discover_flat_structure(self, flat_structure_dir: Path) -> None:
        """Test loading from flat structure (.html and .py in same dir)."""
        registry = SpellBlockRegistry(source=flat_structure_dir, load_builtins=False)
        blocks = registry.list_blocks()
        assert "flatblock" in blocks

    def test_get_block_from_flat_structure(self, flat_structure_dir: Path) -> None:
        """Test retrieving block class from flat structure."""
        registry = SpellBlockRegistry(source=flat_structure_dir, load_builtins=False)
        block_class = registry.get_block("flatblock")
        assert block_class is not None
        assert issubclass(block_class, BaseSpellBlock)

    def test_render_from_flat_structure(self, flat_structure_dir: Path) -> None:
        """Test rendering from flat structure."""
        registry = SpellBlockRegistry(source=flat_structure_dir, load_builtins=False)
        block = registry.create_block("flatblock", content="Flat test")
        assert block is not None
        html = block.render()
        assert "Flat test" in html
        assert "flat-block" in html


class TestRegistryManualConfiguration:
    """Test manual dictionary configuration."""

    def test_manual_dict_configuration(self, standard_structure_dir: Path) -> None:
        """Test loading blocks via manual dictionary."""
        templates_dir = standard_structure_dir / "templates"
        logic_dir = standard_structure_dir / "logic"

        config = {
            "testblock": {
                "logic_file": str(logic_dir / "testblock.py"),
                "template_file": str(templates_dir / "testblock.html"),
            }
        }

        registry = SpellBlockRegistry(source=config, load_builtins=False)
        blocks = registry.list_blocks()
        assert "testblock" in blocks

    def test_manual_config_with_multiple_blocks(self, tmp_path: Path) -> None:
        """Test manual configuration with multiple blocks."""
        # Create two simple blocks
        (tmp_path / "block1.html").write_text("<div>{{ content }}</div>")
        (tmp_path / "block1.py").write_text(
            """
from spellbook_engine import BaseSpellBlock
class Block1Block(BaseSpellBlock):
    pass
"""
        )

        (tmp_path / "block2.html").write_text("<span>{{ content }}</span>")
        (tmp_path / "block2.py").write_text(
            """
from spellbook_engine import BaseSpellBlock
class Block2Block(BaseSpellBlock):
    pass
"""
        )

        config = {
            "block1": {
                "logic_file": str(tmp_path / "block1.py"),
                "template_file": str(tmp_path / "block1.html"),
            },
            "block2": {
                "logic_file": str(tmp_path / "block2.py"),
                "template_file": str(tmp_path / "block2.html"),
            },
        }

        registry = SpellBlockRegistry(source=config, load_builtins=False)
        blocks = registry.list_blocks()
        assert "block1" in blocks
        assert "block2" in blocks

    def test_manual_config_invalid_missing_fields(self) -> None:
        """Test that manual config validates required fields."""
        config = {
            "incomplete": {
                "logic_file": "some/path.py"
                # Missing template_file
            }
        }

        with pytest.raises(ValueError) as exc_info:
            SpellBlockRegistry(source=config, load_builtins=False)

        assert "template_file" in str(exc_info.value)


class TestRegistryErrorHandling:
    """Test error handling in registry."""

    def test_nonexistent_path_raises_error(self) -> None:
        """Test that nonexistent path raises discovery error."""
        with pytest.raises(SpellBlockDiscoveryError):
            SpellBlockRegistry(source="/nonexistent/path", load_builtins=False)

    def test_empty_directory_raises_error(self, tmp_path: Path) -> None:
        """Test that empty directory raises discovery error."""
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()

        with pytest.raises(SpellBlockDiscoveryError):
            SpellBlockRegistry(source=empty_dir, load_builtins=False)

    def test_invalid_source_type_raises_error(self) -> None:
        """Test that invalid source type raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            SpellBlockRegistry(source=123, load_builtins=False)  # type: ignore

        assert "Invalid source type" in str(exc_info.value)

    def test_missing_logic_file_warning(self, tmp_path: Path) -> None:
        """Test that missing logic file is handled gracefully."""
        templates_dir = tmp_path / "templates"
        logic_dir = tmp_path / "logic"
        templates_dir.mkdir()
        logic_dir.mkdir()

        # Create template without corresponding logic file
        (templates_dir / "orphan.html").write_text("<div>{{ content }}</div>")

        # Should not raise error, just log warning
        registry = SpellBlockRegistry(source=tmp_path, load_builtins=False)
        blocks = registry.list_blocks()

        # orphan should not be in the list
        assert "orphan" not in blocks

    def test_invalid_python_file_raises_load_error(self, tmp_path: Path) -> None:
        """Test that invalid Python file raises SpellBlockLoadError."""
        templates_dir = tmp_path / "templates"
        logic_dir = tmp_path / "logic"
        templates_dir.mkdir()
        logic_dir.mkdir()

        (templates_dir / "broken.html").write_text("<div>{{ content }}</div>")
        (logic_dir / "broken.py").write_text("this is not valid python syntax {][")

        with pytest.raises(SpellBlockLoadError):
            SpellBlockRegistry(source=tmp_path, load_builtins=False)


class TestRegistryBlockRetrieval:
    """Test block retrieval methods."""

    def test_get_nonexistent_block_returns_none(self) -> None:
        """Test that getting nonexistent block returns None."""
        registry = SpellBlockRegistry(load_builtins=False)
        block_class = registry.get_block("nonexistent")
        assert block_class is None

    def test_get_nonexistent_template_returns_none(self) -> None:
        """Test that getting nonexistent template returns None."""
        registry = SpellBlockRegistry(load_builtins=False)
        template = registry.get_template("nonexistent")
        assert template is None

    def test_create_nonexistent_block_returns_none(self) -> None:
        """Test that creating nonexistent block returns None."""
        registry = SpellBlockRegistry(load_builtins=False)
        block = registry.create_block("nonexistent")
        assert block is None


class TestBuiltinBlocks:
    """Test built-in SpellBlock functionality."""

    def test_builtins_loaded_by_default(self) -> None:
        """Test that built-in blocks are available."""
        registry = SpellBlockRegistry()
        blocks = registry.list_blocks()

        # Should have at least one built-in
        assert len(blocks) > 0

    def test_create_builtin_alert_block(self) -> None:
        """Test creating built-in alert block."""
        registry = SpellBlockRegistry()

        # Only test if alert is available
        if "alert" in registry.list_blocks():
            block = registry.create_block("alert", content="Test alert", type="info")
            assert block is not None
            html = block.render()
            assert "Test alert" in html

    def test_user_blocks_override_builtins(self, tmp_path: Path) -> None:
        """Test that user blocks can override built-in blocks."""
        # Create user version of a built-in block
        (tmp_path / "alert.html").write_text("<div class='custom-alert'>{{ content }}</div>")
        (tmp_path / "alert.py").write_text(
            """
from spellbook_engine import BaseSpellBlock
class AlertBlock(BaseSpellBlock):
    def get_context(self):
        return {"content": "CUSTOM: " + self.content}
"""
        )

        registry = SpellBlockRegistry(source=tmp_path, load_builtins=True)

        # User's alert should override built-in
        block = registry.create_block("alert", content="Test")
        assert block is not None
        html = block.render()
        assert "CUSTOM: Test" in html
        assert "custom-alert" in html


class TestRegistryEdgeCases:
    """Test edge cases and less common code paths."""

    def test_default_spellblocks_directory_discovery(
        self, tmp_path: Path, monkeypatch: Any
    ) -> None:
        """Test that registry discovers ./spellblocks by default."""
        # Change to temp directory
        monkeypatch.chdir(tmp_path)

        # Create spellblocks directory in current working directory
        spellblocks_dir = tmp_path / "spellblocks"
        spellblocks_dir.mkdir()

        (spellblocks_dir / "default.html").write_text("<div>{{ content }}</div>")
        (spellblocks_dir / "default.py").write_text(
            """
from spellbook_engine import BaseSpellBlock
class DefaultBlock(BaseSpellBlock):
    pass
"""
        )

        # Initialize without source - should discover ./spellblocks
        registry = SpellBlockRegistry(load_builtins=False)
        blocks = registry.list_blocks()
        assert "default" in blocks

    def test_path_is_file_not_directory(self, tmp_path: Path) -> None:
        """Test error when path points to a file instead of directory."""
        file_path = tmp_path / "notadir.txt"
        file_path.write_text("test")

        with pytest.raises(SpellBlockDiscoveryError):
            SpellBlockRegistry(source=file_path, load_builtins=False)

    def test_hybrid_config_with_discover_path(self, tmp_path: Path) -> None:
        """Test manual config with _discover_path for hybrid approach."""
        # Create directory for discovery
        discover_dir = tmp_path / "discover"
        discover_dir.mkdir()
        (discover_dir / "auto.html").write_text("<div>{{ content }}</div>")
        (discover_dir / "auto.py").write_text(
            """
from spellbook_engine import BaseSpellBlock
class AutoBlock(BaseSpellBlock):
    pass
"""
        )

        # Create manual block
        (tmp_path / "manual.html").write_text("<span>{{ content }}</span>")
        (tmp_path / "manual.py").write_text(
            """
from spellbook_engine import BaseSpellBlock
class ManualBlock(BaseSpellBlock):
    pass
"""
        )

        config = {
            "_discover_path": str(discover_dir),
            "manual": {
                "logic_file": str(tmp_path / "manual.py"),
                "template_file": str(tmp_path / "manual.html"),
            },
        }

        registry = SpellBlockRegistry(source=config, load_builtins=False)
        blocks = registry.list_blocks()

        # Should have both discovered and manual blocks
        assert "auto" in blocks
        assert "manual" in blocks

    def test_fallback_class_name_discovery(self, tmp_path: Path) -> None:
        """Test that blocks with non-standard class names are discovered."""
        (tmp_path / "weird.html").write_text("<div>{{ content }}</div>")
        (tmp_path / "weird.py").write_text(
            """
from spellbook_engine import BaseSpellBlock
# Non-standard class name (not WeirdBlock)
class MyCustomBlockClass(BaseSpellBlock):
    pass
"""
        )

        registry = SpellBlockRegistry(source=tmp_path, load_builtins=False)
        blocks = registry.list_blocks()
        assert "weird" in blocks

        # Should be able to create block
        block = registry.create_block("weird", content="Test")
        assert block is not None

    def test_block_class_not_found(self, tmp_path: Path) -> None:
        """Test error when Python file has no suitable block class."""
        templates_dir = tmp_path / "templates"
        logic_dir = tmp_path / "logic"
        templates_dir.mkdir()
        logic_dir.mkdir()

        (templates_dir / "noclass.html").write_text("<div>{{ content }}</div>")
        (logic_dir / "noclass.py").write_text(
            """
# Python file with no block class
def some_function():
    pass
"""
        )

        with pytest.raises(SpellBlockLoadError) as exc_info:
            SpellBlockRegistry(source=tmp_path, load_builtins=False)

        assert "No suitable block class found" in str(exc_info.value)

    def test_get_template_when_no_jinja_env(self) -> None:
        """Test get_template returns None when jinja_env is not set."""
        registry = SpellBlockRegistry(load_builtins=False)
        # Manually clear jinja env to test edge case
        registry._jinja_env = None

        template = registry.get_template("anything")
        assert template is None

    def test_create_block_when_template_missing(self, tmp_path: Path) -> None:
        """Test create_block returns None when template can't be retrieved."""
        (tmp_path / "notemplate.py").write_text(
            """
from spellbook_engine import BaseSpellBlock
class NotemplateBlock(BaseSpellBlock):
    pass
"""
        )

        registry = SpellBlockRegistry(source=tmp_path, load_builtins=False)

        # Manually remove template to test edge case
        if "notemplate" in registry._blocks:
            registry._blocks["notemplate"]["template_name"] = "nonexistent.html"

        block = registry.create_block("notemplate", content="Test")
        # Should return None because template can't be found
        assert block is None
