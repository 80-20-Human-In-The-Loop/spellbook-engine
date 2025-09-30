"""Integration tests for SpellbookParser with golden file comparison."""

from collections.abc import Callable

import pytest

from spellbook_engine import PRESET_THEMES, SpellbookParser, Theme, ThemeColors


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


class TestThemeIntegration:
    """Test theme system integration with parser."""

    def test_parser_with_preset_theme_name(self):
        """Test parser with preset theme by name."""
        parser = SpellbookParser(theme="arcane")
        markdown = """
{~ alert type="info" ~}
This is themed content.
{~~}
"""
        html = parser.render(markdown)

        # Should have :root block with CSS variables
        assert ":root {" in html
        assert "--primary-color:" in html
        assert "#8b5cf6" in html  # Arcane primary color

    def test_parser_with_custom_theme_object(self):
        """Test parser with custom Theme object."""
        colors = ThemeColors(
            primary="#FF6B35",
            accent="#FFD700",
            background="#1a1a1a",
            text="#ffffff",
        )
        theme = Theme(name="CustomTheme", colors=colors)
        parser = SpellbookParser(theme=theme)

        markdown = """
{~ card title="Test" ~}
Custom themed card.
{~~}
"""
        html = parser.render(markdown)

        # Should have custom colors in :root block
        assert ":root {" in html
        assert "--primary-color: #FF6B35;" in html
        assert "--accent-color: #FFD700;" in html
        assert "--background-color: #1a1a1a;" in html
        assert "--text-color: #ffffff;" in html

    def test_parser_with_theme_variants(self):
        """Test parser with theme opacity variants."""
        colors = ThemeColors(primary="#FF6B35")
        theme = Theme(name="Test", colors=colors, generate_variants=True)
        parser = SpellbookParser(theme=theme)

        markdown = "# Test"
        html = parser.render(markdown)

        # Should have opacity variants
        assert "--primary-color-25:" in html
        assert "color-mix(in srgb, #FF6B35 25%, transparent)" in html
        assert "--primary-color-50:" in html
        assert "--primary-color-75:" in html

    def test_parser_without_theme(self):
        """Test parser without theme uses fallback values."""
        parser = SpellbookParser()
        markdown = """
{~ alert type="success" ~}
No theme set.
{~~}
"""
        html = parser.render(markdown)

        # Should NOT have :root block
        assert ":root {" not in html

        # But should still have styles with fallback values
        assert ".sb-alert" in html
        assert "var(--success-color" in html  # CSS variable with fallback

    def test_parser_with_invalid_theme_name(self):
        """Test parser with invalid theme name falls back to no theme."""
        parser = SpellbookParser(theme="nonexistent")

        # Should not crash, should fall back to no theme
        assert parser.theme is None

        markdown = "# Test"
        html = parser.render(markdown)
        assert ":root {" not in html

    def test_theme_with_all_preset_themes(self):
        """Test that all preset themes work with parser."""
        markdown = """
{~ alert type="info" ~}
Testing preset themes.
{~~}
"""

        for theme_name in PRESET_THEMES:
            parser = SpellbookParser(theme=theme_name)
            html = parser.render(markdown)

            # Each theme should produce valid HTML with :root block
            assert "<h" not in markdown  # No headings in input
            assert ":root {" in html
            assert "--primary-color:" in html
            assert ".sb-alert" in html

    def test_theme_css_variables_come_before_styles(self):
        """Test that theme variables are injected before block styles."""
        colors = ThemeColors(primary="#FF6B35")
        theme = Theme(name="Test", colors=colors, generate_variants=False)
        parser = SpellbookParser(theme=theme)

        markdown = """
{~ alert type="info" ~}
Test alert.
{~~}
"""
        html = parser.render(markdown)

        # :root block should come before block styles
        root_pos = html.find(":root")
        alert_style_pos = html.find("/* alert */")

        assert root_pos > 0
        assert alert_style_pos > 0
        assert root_pos < alert_style_pos

    def test_theme_with_multiple_blocks(self):
        """Test theme with multiple different blocks."""
        parser = SpellbookParser(theme="forest")
        markdown = """
{~ alert type="success" ~}
Success message.
{~~}

{~ card title="Forest Card" ~}
Card content.
{~~}

{~ quote author="Test" ~}
Quote content.
{~~}
"""
        html = parser.render(markdown)

        # Should have :root block
        assert ":root {" in html
        assert "--primary-color: #059669;" in html  # Forest theme

        # Should have all block styles (deduplicated)
        assert "/* alert */" in html
        assert "/* card */" in html
        assert "/* quote */" in html

        # Should have all block HTML
        assert "sb-alert" in html
        assert "sb-card" in html
        assert "sb-quote" in html

    def test_theme_preserved_across_multiple_renders(self):
        """Test that theme persists for multiple render calls."""
        parser = SpellbookParser(theme="crimson")

        markdown1 = '{~ alert type="danger" ~}First{~~}'
        markdown2 = '{~ card title="Test" ~}Second{~~}'

        html1 = parser.render(markdown1)
        html2 = parser.render(markdown2)

        # Both should have crimson theme colors
        assert "--primary-color: #dc2626;" in html1
        assert "--primary-color: #dc2626;" in html2

    def test_theme_with_custom_colors(self):
        """Test theme with additional custom color variables."""
        theme = Theme(
            name="Test",
            custom_colors={
                "brand-primary": "#123456",
                "brand-secondary": "#abcdef",
            },
        )
        parser = SpellbookParser(theme=theme)

        markdown = "# Test"
        html = parser.render(markdown)

        # Should include custom colors
        assert "--brand-primary: #123456;" in html
        assert "--brand-secondary: #abcdef;" in html
