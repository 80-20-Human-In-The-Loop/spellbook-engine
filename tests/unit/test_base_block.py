"""Unit tests for BaseSpellBlock."""

from typing import Any

from jinja2 import Template

from spellbook_engine import BaseSpellBlock


class TestBaseSpellBlockInitialization:
    """Test BaseSpellBlock initialization."""

    def test_init_with_defaults(self) -> None:
        """Test initialization with default values."""
        block = BaseSpellBlock()
        assert block.content == ""
        assert block.template is None
        assert block.kwargs == {}

    def test_init_with_content(self) -> None:
        """Test initialization with content."""
        block = BaseSpellBlock(content="Hello World")
        assert block.content == "Hello World"

    def test_init_with_template(self, mock_template: Template) -> None:
        """Test initialization with a template."""
        block = BaseSpellBlock(template=mock_template)
        assert block.template == mock_template

    def test_init_with_kwargs(self) -> None:
        """Test initialization with keyword arguments."""
        block = BaseSpellBlock(content="Test", title="My Title", css_class="custom-class")
        assert block.content == "Test"
        assert block.kwargs["title"] == "My Title"
        assert block.kwargs["css_class"] == "custom-class"


class TestBaseSpellBlockContext:
    """Test BaseSpellBlock context generation."""

    def test_get_context_default(self) -> None:
        """Test default context generation."""
        block = BaseSpellBlock(content="Test content")
        context = block.get_context()
        assert "content" in context
        # Content is now processed as markdown (wrapped in <p> tags)
        assert context["content"] == "<p>Test content</p>"

    def test_get_context_includes_kwargs(self) -> None:
        """Test that context includes all kwargs."""
        block = BaseSpellBlock(content="Test", title="Title", css_class="custom", active=True)
        context = block.get_context()
        assert context["title"] == "Title"
        assert context["css_class"] == "custom"
        assert context["active"] is True

    def test_process_content_default(self) -> None:
        """Test that process_content processes markdown by default."""
        block = BaseSpellBlock(content="Original content")
        processed = block.process_content()
        # Content is now processed as markdown
        assert processed == "<p>Original content</p>"


class TestBaseSpellBlockRendering:
    """Test BaseSpellBlock rendering functionality."""

    def test_render_with_template(self, mock_template: Template) -> None:
        """Test rendering with a valid template."""
        block = BaseSpellBlock(content="Hello World", template=mock_template)
        html = block.render()
        # Content is processed as markdown (wrapped in <p> tags)
        assert "<div class='test'><p>Hello World</p></div>" in html

    def test_render_with_template_and_vars(self, mock_template_with_vars: Template) -> None:
        """Test rendering with template that uses multiple variables."""
        block = BaseSpellBlock(
            content="Body text",
            template=mock_template_with_vars,
            title="My Title",
            css_class="custom-class",
            element_id="test-id",
        )
        html = block.render()
        assert "My Title" in html
        assert "Body text" in html
        assert 'class="custom-class"' in html
        assert 'id="test-id"' in html

    def test_render_without_template(self) -> None:
        """Test rendering fallback when no template is provided."""
        block = BaseSpellBlock(content="Fallback content")
        html = block.render()
        # Should return processed content directly (now as HTML)
        assert html == "<p>Fallback content</p>"

    def test_render_with_template_error(self) -> None:
        """Test rendering when template raises an error."""
        bad_template = Template("{{ undefined_var.missing_attribute }}")
        block = BaseSpellBlock(template=bad_template)
        html = block.render()
        # Should return error comment
        assert "<!-- Error rendering block:" in html

    def test_str_method(self, mock_template: Template) -> None:
        """Test that __str__ returns rendered content."""
        block = BaseSpellBlock(content="String test", template=mock_template)
        assert str(block) == block.render()


class TestBaseSpellBlockProcessMethod:
    """Test BaseSpellBlock process method."""

    def test_process_updates_content(self) -> None:
        """Test that process method updates content."""
        block = BaseSpellBlock(content="Original")
        result = block.process("New content")
        assert block.content == "New content"
        assert result is block  # Should return self for chaining

    def test_process_chaining(self) -> None:
        """Test that process method allows chaining."""
        block = BaseSpellBlock()
        result = block.process("Test").process("Updated")
        assert result is block
        assert block.content == "Updated"


class CustomSpellBlock(BaseSpellBlock):
    """Custom SpellBlock for testing inheritance."""

    def process_content(self) -> str:
        """Custom content processing that uppercases content."""
        return self.content.upper()

    def get_context(self) -> dict[str, Any]:
        """Custom context with additional processing."""
        context = super().get_context()
        context["custom_field"] = "custom_value"
        return context


class TestCustomSpellBlock:
    """Test custom SpellBlock implementation."""

    def test_custom_process_content(self) -> None:
        """Test that custom process_content is used."""
        block = CustomSpellBlock(content="hello world")
        assert block.process_content() == "HELLO WORLD"

    def test_custom_get_context(self) -> None:
        """Test that custom get_context adds fields."""
        block = CustomSpellBlock(content="test")
        context = block.get_context()
        assert "content" in context
        assert context["content"] == "TEST"  # Uppercased by custom processor
        assert context["custom_field"] == "custom_value"

    def test_custom_render(self, mock_template: Template) -> None:
        """Test that custom processing is used during rendering."""
        block = CustomSpellBlock(content="hello", template=mock_template)
        html = block.render()
        assert "HELLO" in html  # Content should be uppercased
