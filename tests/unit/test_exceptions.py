"""Unit tests for custom exceptions."""

from pathlib import Path

import pytest

from spellbook_engine.exceptions import (
    ParserError,
    SpellBlockDiscoveryError,
    SpellBlockLoadError,
    SpellBlockRenderError,
    SpellbookError,
)


class TestSpellbookError:
    """Test base SpellbookError exception."""

    def test_base_exception(self) -> None:
        """Test that SpellbookError can be raised."""
        with pytest.raises(SpellbookError) as exc_info:
            raise SpellbookError("Base error")
        assert "Base error" in str(exc_info.value)


class TestSpellBlockDiscoveryError:
    """Test SpellBlockDiscoveryError exception."""

    def test_error_without_path(self) -> None:
        """Test error message when no path is provided."""
        with pytest.raises(SpellBlockDiscoveryError) as exc_info:
            raise SpellBlockDiscoveryError()

        error_msg = str(exc_info.value)
        assert "No SpellBlocks directory found" in error_msg
        assert "spellblocks" in error_msg
        assert "Create a 'spellblocks' folder" in error_msg
        assert "SpellBlockRegistry('path/to/blocks')" in error_msg
        assert "templates/" in error_msg
        assert "logic/" in error_msg

    def test_error_with_nonexistent_path(self, tmp_path: Path) -> None:
        """Test error message with a non-existent path."""
        nonexistent = tmp_path / "does_not_exist"
        with pytest.raises(SpellBlockDiscoveryError) as exc_info:
            raise SpellBlockDiscoveryError(nonexistent)

        error_msg = str(exc_info.value)
        assert str(nonexistent) in error_msg
        assert "Invalid SpellBlocks directory structure" in error_msg
        assert "Directory does not exist" in error_msg

    def test_error_with_empty_directory(self, tmp_path: Path) -> None:
        """Test error message with an empty directory."""
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()

        with pytest.raises(SpellBlockDiscoveryError) as exc_info:
            raise SpellBlockDiscoveryError(empty_dir)

        error_msg = str(exc_info.value)
        assert str(empty_dir) in error_msg
        assert "Directory is empty" in error_msg

    def test_error_with_populated_directory(self, tmp_path: Path) -> None:
        """Test error message lists directory contents."""
        test_dir = tmp_path / "test"
        test_dir.mkdir()
        (test_dir / "file1.txt").write_text("test")
        (test_dir / "file2.txt").write_text("test")
        (test_dir / "subdir").mkdir()

        with pytest.raises(SpellBlockDiscoveryError) as exc_info:
            raise SpellBlockDiscoveryError(test_dir)

        error_msg = str(exc_info.value)
        assert "file1.txt" in error_msg
        assert "file2.txt" in error_msg
        assert "subdir/" in error_msg

    def test_error_with_file_instead_of_directory(self, tmp_path: Path) -> None:
        """Test error message when path is a file, not a directory."""
        file_path = tmp_path / "file.txt"
        file_path.write_text("test")

        with pytest.raises(SpellBlockDiscoveryError) as exc_info:
            raise SpellBlockDiscoveryError(file_path)

        error_msg = str(exc_info.value)
        assert "Path is not a directory" in error_msg

    def test_error_limits_directory_listing(self, tmp_path: Path) -> None:
        """Test that directory listing is limited to first 10 items."""
        test_dir = tmp_path / "many_files"
        test_dir.mkdir()

        # Create 15 files
        for i in range(15):
            (test_dir / f"file{i:02d}.txt").write_text("test")

        with pytest.raises(SpellBlockDiscoveryError) as exc_info:
            raise SpellBlockDiscoveryError(test_dir)

        error_msg = str(exc_info.value)
        assert "... and more" in error_msg


class TestSpellBlockLoadError:
    """Test SpellBlockLoadError exception."""

    def test_load_error_message(self) -> None:
        """Test load error message format."""
        with pytest.raises(SpellBlockLoadError) as exc_info:
            raise SpellBlockLoadError("testblock", "File not found")

        error_msg = str(exc_info.value)
        assert "Failed to load SpellBlock 'testblock'" in error_msg
        assert "File not found" in error_msg
        assert "Please check:" in error_msg
        assert "TestblockBlock" in error_msg  # Capitalized class name
        assert "syntax errors" in error_msg

    def test_load_error_includes_block_name(self) -> None:
        """Test that block name is properly included."""
        with pytest.raises(SpellBlockLoadError) as exc_info:
            raise SpellBlockLoadError("myblock", "Some reason")

        error_msg = str(exc_info.value)
        assert "myblock" in error_msg
        assert "MyblockBlock" in error_msg


class TestSpellBlockRenderError:
    """Test SpellBlockRenderError exception."""

    def test_render_error_message(self) -> None:
        """Test render error message format."""
        with pytest.raises(SpellBlockRenderError) as exc_info:
            raise SpellBlockRenderError("alert", "Template syntax error")

        error_msg = str(exc_info.value)
        assert "Failed to render SpellBlock 'alert'" in error_msg
        assert "Template syntax error" in error_msg

    def test_render_error_with_different_reason(self) -> None:
        """Test render error with different reason."""
        with pytest.raises(SpellBlockRenderError) as exc_info:
            raise SpellBlockRenderError("card", "Missing required field: title")

        error_msg = str(exc_info.value)
        assert "card" in error_msg
        assert "Missing required field: title" in error_msg


class TestParserError:
    """Test ParserError exception."""

    def test_parser_error(self) -> None:
        """Test that ParserError can be raised."""
        with pytest.raises(ParserError) as exc_info:
            raise ParserError("Invalid markdown syntax")

        error_msg = str(exc_info.value)
        assert "Invalid markdown syntax" in error_msg

    def test_parser_error_inherits_from_spellbook_error(self) -> None:
        """Test that ParserError inherits from SpellbookError."""
        with pytest.raises(SpellbookError):
            raise ParserError("Parser failed")


class TestExceptionHierarchy:
    """Test exception inheritance hierarchy."""

    def test_all_exceptions_inherit_from_base(self) -> None:
        """Test that all custom exceptions inherit from SpellbookError."""
        exceptions = [
            SpellBlockDiscoveryError(),
            SpellBlockLoadError("test", "reason"),
            SpellBlockRenderError("test", "reason"),
            ParserError("error"),
        ]

        for exc in exceptions:
            assert isinstance(exc, SpellbookError)

    def test_can_catch_all_with_base_exception(self) -> None:
        """Test that base exception catches all custom exceptions."""
        with pytest.raises(SpellbookError):
            raise SpellBlockLoadError("test", "reason")

        with pytest.raises(SpellbookError):
            raise SpellBlockDiscoveryError()

        with pytest.raises(SpellbookError):
            raise ParserError("error")
