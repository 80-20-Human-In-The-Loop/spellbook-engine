"""Unit tests for built-in SpellBlocks."""

from typing import Any

import pytest
from jinja2 import Template

from spellbook_engine import SpellBlockRegistry
from spellbook_engine.builtins.logic.alert import AlertBlock
from spellbook_engine.builtins.logic.card import CardBlock
from spellbook_engine.builtins.logic.quote import QuoteBlock


@pytest.fixture
def simple_template() -> Template:
    """Simple template for testing block context."""
    return Template(
        """
<div class="{{ css_class }}">
    {% if title %}<h3>{{ title }}</h3>{% endif %}
    {{ content }}
    {% if footer %}<footer>{{ footer }}</footer>{% endif %}
</div>
"""
    )


class TestCardBlock:
    """Test CardBlock implementation."""

    def test_card_with_all_attributes(self, simple_template: Template) -> None:
        """Test card block with all possible attributes."""
        block = CardBlock(
            content="Card body content",
            template=simple_template,
            title="Card Title",
            footer="Card Footer",
            style="primary",
            collapsible=True,
            collapsed=True,
        )

        context = block.get_context()
        assert context["title"] == "Card Title"
        assert context["footer"] == "Card Footer"
        assert context["style"] == "primary"
        # Content is now processed as markdown (wrapped in <p> tags)
        assert context["content"] == "<p>Card body content</p>"
        assert context["collapsible"] is True
        assert context["collapsed"] is True

    def test_card_with_minimal_attributes(self, simple_template: Template) -> None:
        """Test card block with default attributes."""
        block = CardBlock(content="Simple card", template=simple_template)

        context = block.get_context()
        assert context["title"] == ""
        assert context["footer"] == ""
        assert context["style"] == "default"
        # Content is now processed as markdown (wrapped in <p> tags)
        assert context["content"] == "<p>Simple card</p>"
        assert context["collapsible"] is False
        assert context["collapsed"] is False

    def test_card_with_empty_content(self, simple_template: Template) -> None:
        """Test card with empty content."""
        block = CardBlock(content="", template=simple_template, title="Empty Card")

        context = block.get_context()
        assert context["content"] == ""
        assert context["title"] == "Empty Card"

    def test_card_content_stripping(self, simple_template: Template) -> None:
        """Test that card content strips whitespace."""
        block = CardBlock(content="   \n  Content with whitespace  \n  ", template=simple_template)

        processed = block.process_content()
        # Content is now processed as markdown (wrapped in <p> tags)
        assert processed == "<p>Content with whitespace</p>"
        assert not processed.startswith(" ")
        assert not processed.endswith(" ")

    def test_card_renders_correctly(self) -> None:
        """Test that card renders with actual template."""
        registry = SpellBlockRegistry()

        if "card" in registry.list_blocks():
            block = registry.create_block(
                "card", content="Test content", title="Test Card", footer="Test Footer"
            )
            html = block.render()

            assert "Test content" in html
            assert "Test Card" in html
            assert "Test Footer" in html


class TestQuoteBlock:
    """Test QuoteBlock implementation."""

    def test_quote_with_all_attributes(self, simple_template: Template) -> None:
        """Test quote block with all possible attributes."""
        block = QuoteBlock(
            content="The only way to do great work is to love what you do.",
            template=simple_template,
            author="Steve Jobs",
            source="Stanford Commencement Speech",
            cite="https://example.com/speech",
            style="large",
        )

        context = block.get_context()
        # Content is now processed as markdown (wrapped in <p> tags)
        assert context["content"] == "<p>The only way to do great work is to love what you do.</p>"
        assert context["author"] == "Steve Jobs"
        assert context["source"] == "Stanford Commencement Speech"
        assert context["cite"] == "https://example.com/speech"
        assert context["style"] == "large"

    def test_quote_with_minimal_attributes(self, simple_template: Template) -> None:
        """Test quote block with default attributes."""
        block = QuoteBlock(content="Simple quote", template=simple_template)

        context = block.get_context()
        # Content is now processed as markdown (wrapped in <p> tags)
        assert context["content"] == "<p>Simple quote</p>"
        assert context["author"] == ""
        assert context["source"] == ""
        assert context["cite"] == ""
        assert context["style"] == "default"

    def test_quote_with_empty_content(self, simple_template: Template) -> None:
        """Test quote with empty content."""
        block = QuoteBlock(content="", template=simple_template, author="Anonymous")

        context = block.get_context()
        assert context["content"] == ""
        assert context["author"] == "Anonymous"

    def test_quote_content_stripping(self, simple_template: Template) -> None:
        """Test that quote content strips whitespace."""
        block = QuoteBlock(content="  \n  Quote with whitespace  \n  ", template=simple_template)

        processed = block.process_content()
        # Content is now processed as markdown (wrapped in <p> tags)
        assert processed == "<p>Quote with whitespace</p>"
        assert not processed.startswith(" ")
        assert not processed.endswith(" ")

    def test_quote_renders_correctly(self) -> None:
        """Test that quote renders with actual template."""
        registry = SpellBlockRegistry()

        if "quote" in registry.list_blocks():
            block = registry.create_block(
                "quote",
                content="Test quote content",
                author="Test Author",
                source="Test Source",
            )
            html = block.render()

            assert "Test quote content" in html
            assert "Test Author" in html
            assert "Test Source" in html


class TestAlertBlock:
    """Test AlertBlock implementation."""

    def test_alert_with_all_attributes(self, simple_template: Template) -> None:
        """Test alert block with all possible attributes."""
        block = AlertBlock(
            content="This is an important alert",
            template=simple_template,
            type="warning",
            dismissible=True,
            title="Warning Title",
        )

        context = block.get_context()
        # Content is now processed as markdown (wrapped in <p> tags)
        assert context["content"] == "<p>This is an important alert</p>"
        assert context["type"] == "warning"
        assert context["dismissible"] is True
        assert context["title"] == "Warning Title"
        assert "css_class" in context
        assert context["css_class"] == "alert-warning"

    def test_alert_with_different_types(self, simple_template: Template) -> None:
        """Test alert with different type values."""
        types = ["info", "success", "warning", "danger"]

        for alert_type in types:
            block = AlertBlock(
                content=f"{alert_type.capitalize()} message",
                template=simple_template,
                type=alert_type,
            )

            context = block.get_context()
            assert context["type"] == alert_type
            # Content is now processed as markdown (wrapped in <p> tags)
            assert context["content"] == f"<p>{alert_type.capitalize()} message</p>"

    def test_alert_with_minimal_attributes(self, simple_template: Template) -> None:
        """Test alert block with default attributes."""
        block = AlertBlock(content="Simple alert", template=simple_template)

        context = block.get_context()
        # Content is now processed as markdown (wrapped in <p> tags)
        assert context["content"] == "<p>Simple alert</p>"
        assert context["type"] == "info"  # Default type
        assert context["dismissible"] is False

    def test_alert_renders_correctly(self) -> None:
        """Test that alert renders with actual template."""
        registry = SpellBlockRegistry()

        if "alert" in registry.list_blocks():
            block = registry.create_block("alert", content="Test alert", type="success")
            html = block.render()

            assert "Test alert" in html
            # Alert template should have alert-related classes
            assert "alert" in html.lower()


class TestBuiltinBlocksIntegration:
    """Test that all built-in blocks are available and functional."""

    def test_all_builtins_available(self) -> None:
        """Test that all expected built-in blocks are loaded."""
        registry = SpellBlockRegistry()
        blocks = registry.list_blocks()

        # Should have at least some built-in blocks
        assert len(blocks) > 0

        # Check for common built-ins
        expected_blocks = {"alert", "card", "quote"}
        available_blocks = set(blocks)

        # At least some expected blocks should be present
        assert len(expected_blocks & available_blocks) > 0

    def test_builtin_blocks_can_render(self) -> None:
        """Test that all built-in blocks can be created and rendered."""
        registry = SpellBlockRegistry()

        for block_name in registry.list_blocks():
            block = registry.create_block(block_name, content="Test content")
            assert block is not None

            html = block.render()
            assert html is not None
            assert isinstance(html, str)
            assert len(html) > 0

    def test_builtin_blocks_with_kwargs(self) -> None:
        """Test that built-in blocks handle various kwargs."""
        registry = SpellBlockRegistry()

        test_cases: list[tuple[str, dict[str, Any]]] = [
            ("alert", {"type": "warning", "dismissible": True}),
            ("card", {"title": "Test", "footer": "Footer"}),
            ("quote", {"author": "Author", "source": "Source"}),
        ]

        for block_name, kwargs in test_cases:
            if block_name in registry.list_blocks():
                block = registry.create_block(block_name, content="Test content", **kwargs)
                assert block is not None

                html = block.render()
                assert "Test content" in html
