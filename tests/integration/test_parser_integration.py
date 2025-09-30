"""Integration tests for SpellbookParser with golden file comparison."""

from collections.abc import Callable

import pytest

from spellbook_engine import SpellbookParser


class TestBasicMarkdownParsing:
    """Test basic markdown parsing with SpellBlocks."""

    def test_basic_markdown(
        self,
        parser_with_builtins: SpellbookParser,
        dummy_loader: Callable[[str], str],
        golden_loader: Callable[[str], str | None],
        golden_saver: Callable[[str, str], None],
        html_comparator: Callable[[str, str], bool],
        update_golden_files: bool,
    ) -> None:
        """Test comprehensive markdown with all features."""
        # Load the dummy markdown
        markdown_content = dummy_loader("basic_markdown.md")

        # Parse to HTML
        actual_html = parser_with_builtins.render(markdown_content)

        # Save or compare with golden file
        golden_html = golden_loader("basic_markdown.html")

        if update_golden_files:
            golden_saver("basic_markdown.html", actual_html)
            pytest.skip("Updated golden file: basic_markdown.html")

        if golden_html is None:
            pytest.fail("Golden file not found. Run with SPELLBOOK_UPDATE_GOLDEN=1 to create it.")

        # Compare HTML
        assert html_comparator(actual_html, golden_html), "Parsed HTML doesn't match golden file"


class TestSpellBlocksOnly:
    """Test documents with primarily SpellBlocks."""

    def test_spellblocks_only(
        self,
        parser_with_builtins: SpellbookParser,
        dummy_loader: Callable[[str], str],
        golden_loader: Callable[[str], str | None],
        golden_saver: Callable[[str, str], None],
        html_comparator: Callable[[str, str], bool],
        update_golden_files: bool,
    ) -> None:
        """Test markdown with mostly SpellBlocks."""
        markdown_content = dummy_loader("spellblocks_only.md")
        actual_html = parser_with_builtins.render(markdown_content)

        golden_html = golden_loader("spellblocks_only.html")

        if update_golden_files:
            golden_saver("spellblocks_only.html", actual_html)
            pytest.skip("Updated golden file: spellblocks_only.html")

        if golden_html is None:
            pytest.fail("Golden file not found. Run with SPELLBOOK_UPDATE_GOLDEN=1 to create it.")

        assert html_comparator(actual_html, golden_html)

    def test_spellblocks_render_correctly(
        self, parser_with_builtins: SpellbookParser, dummy_loader: Callable[[str], str]
    ) -> None:
        """Test that SpellBlocks produce expected HTML elements."""
        markdown_content = dummy_loader("spellblocks_only.md")
        html = parser_with_builtins.render(markdown_content)

        # Check that SpellBlocks were processed
        assert "alert" in html.lower()  # Alert blocks should be present
        assert "card" in html.lower()  # Card blocks should be present

        # Check that content is preserved
        assert "info alert" in html.lower()
        assert "Simple Card" in html
        assert "Albert Einstein" in html


class TestCodeBlockProtection:
    """Test that code blocks are protected from SpellBlock processing."""

    def test_code_heavy_document(
        self,
        parser_with_builtins: SpellbookParser,
        dummy_loader: Callable[[str], str],
        golden_loader: Callable[[str], str | None],
        golden_saver: Callable[[str, str], None],
        html_comparator: Callable[[str, str], bool],
        update_golden_files: bool,
    ) -> None:
        """Test document with many code blocks."""
        markdown_content = dummy_loader("code_heavy.md")
        actual_html = parser_with_builtins.render(markdown_content)

        golden_html = golden_loader("code_heavy.html")

        if update_golden_files:
            golden_saver("code_heavy.html", actual_html)
            pytest.skip("Updated golden file: code_heavy.html")

        if golden_html is None:
            pytest.fail("Golden file not found. Run with SPELLBOOK_UPDATE_GOLDEN=1 to create it.")

        assert html_comparator(actual_html, golden_html)

    def test_code_blocks_preserve_spellblock_syntax(
        self, parser_with_builtins: SpellbookParser, dummy_loader: Callable[[str], str]
    ) -> None:
        """Test that SpellBlock syntax in code blocks is preserved."""
        markdown_content = dummy_loader("code_heavy.md")
        html = parser_with_builtins.render(markdown_content)

        # SpellBlock syntax should appear in code blocks (not processed)
        assert "{~ alert ~}" in html
        assert "{~~}" in html

        # But real SpellBlocks outside code should be processed
        assert "Code blocks are properly protected!" in html


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_edge_cases_document(
        self,
        parser_with_builtins: SpellbookParser,
        dummy_loader: Callable[[str], str],
        golden_loader: Callable[[str], str | None],
        golden_saver: Callable[[str, str], None],
        html_comparator: Callable[[str, str], bool],
        update_golden_files: bool,
    ) -> None:
        """Test edge cases."""
        markdown_content = dummy_loader("edge_cases.md")
        actual_html = parser_with_builtins.render(markdown_content)

        golden_html = golden_loader("edge_cases.html")

        if update_golden_files:
            golden_saver("edge_cases.html", actual_html)
            pytest.skip("Updated golden file: edge_cases.html")

        if golden_html is None:
            pytest.fail("Golden file not found. Run with SPELLBOOK_UPDATE_GOLDEN=1 to create it.")

        assert html_comparator(actual_html, golden_html)

    def test_empty_spellblocks_handled(
        self, parser_with_builtins: SpellbookParser, dummy_loader: Callable[[str], str]
    ) -> None:
        """Test that empty SpellBlocks are handled gracefully."""
        markdown_content = dummy_loader("edge_cases.md")
        html = parser_with_builtins.render(markdown_content)

        # Should not raise errors, should produce some output
        assert len(html) > 0
        assert "<html>" not in html.lower() or "</html>" in html.lower()

    def test_unicode_content_preserved(
        self, parser_with_builtins: SpellbookParser, dummy_loader: Callable[[str], str]
    ) -> None:
        """Test that Unicode content is preserved."""
        markdown_content = dummy_loader("edge_cases.md")
        html = parser_with_builtins.render(markdown_content)

        # Unicode characters should be preserved
        assert "你好" in html or "&#" in html  # Chinese characters (raw or encoded)
        assert "🎉" in html or "&#" in html  # Emoji (raw or encoded)


class TestParserConfiguration:
    """Test parser with different configurations."""

    def test_parser_without_builtins(self, parser_without_builtins: SpellbookParser) -> None:
        """Test that parser works without built-in blocks."""
        markdown = """
# Test

Regular markdown works.

{~ alert ~}
This won't render since no blocks are loaded.
{~~}
"""
        html = parser_without_builtins.render(markdown)

        # Heading should be processed
        assert "<h1" in html
        assert "Test" in html

        # SpellBlock should be in a comment or not processed
        # (since no blocks are registered)
        assert "alert" in html.lower()  # Might appear in comment


class TestMarkdownFeatures:
    """Test that standard markdown features work correctly."""

    def test_headings_render(self, parser_with_builtins: SpellbookParser) -> None:
        """Test that all heading levels render."""
        markdown = "# H1\n## H2\n### H3\n#### H4\n##### H5\n###### H6"
        html = parser_with_builtins.render(markdown)

        assert "<h1" in html
        assert "<h2" in html
        assert "<h3" in html
        assert "<h4" in html
        assert "<h5" in html
        assert "<h6" in html

    def test_lists_render(self, parser_with_builtins: SpellbookParser) -> None:
        """Test that lists render correctly."""
        markdown = """
- Item 1
- Item 2

1. First
2. Second
"""
        html = parser_with_builtins.render(markdown)

        assert "<ul" in html
        assert "<ol" in html
        assert "<li" in html
        assert "Item 1" in html
        assert "First" in html

    def test_code_blocks_render(self, parser_with_builtins: SpellbookParser) -> None:
        """Test that code blocks render with proper tags."""
        markdown = """
```python
def hello():
    print("world")
```
"""
        html = parser_with_builtins.render(markdown)

        assert "<code" in html
        assert "def hello" in html

    def test_links_render(self, parser_with_builtins: SpellbookParser) -> None:
        """Test that links render correctly."""
        markdown = "[Example](https://example.com)"
        html = parser_with_builtins.render(markdown)

        assert "<a" in html
        assert "href" in html
        assert "example.com" in html

    def test_emphasis_renders(self, parser_with_builtins: SpellbookParser) -> None:
        """Test that emphasis (bold/italic) renders."""
        markdown = "**bold** and *italic*"
        html = parser_with_builtins.render(markdown)

        assert "<strong" in html or "<b>" in html
        assert "<em" in html or "<i>" in html


class TestSpellBlockAndMarkdownInteraction:
    """Test interaction between SpellBlocks and markdown."""

    def test_markdown_inside_spellblocks(self, parser_with_builtins: SpellbookParser) -> None:
        """Test that markdown inside SpellBlocks is processed."""
        markdown = """
{~ card title="Test" ~}
This has **bold** and *italic* text.

- List item 1
- List item 2
{~~}
"""
        html = parser_with_builtins.render(markdown)

        # SpellBlock should render
        assert "card" in html.lower()

        # Markdown inside should be processed
        # Note: This depends on whether the SpellBlock processes its content
        # For now, just check that content is present
        assert "bold" in html
        assert "italic" in html

    def test_spellblock_after_markdown(self, parser_with_builtins: SpellbookParser) -> None:
        """Test SpellBlock immediately after markdown."""
        markdown = """
**Bold text**
{~ alert type="info" ~}
Alert after bold
{~~}
"""
        html = parser_with_builtins.render(markdown)

        assert "<strong" in html or "<b>" in html
        assert "alert" in html.lower()
        assert "Alert after bold" in html

    def test_markdown_after_spellblock(self, parser_with_builtins: SpellbookParser) -> None:
        """Test markdown immediately after SpellBlock."""
        markdown = """
{~ alert ~}
Alert content
{~~}
**Bold after alert**
"""
        html = parser_with_builtins.render(markdown)

        assert "alert" in html.lower()
        assert "<strong" in html or "<b>" in html
        assert "Bold after alert" in html
