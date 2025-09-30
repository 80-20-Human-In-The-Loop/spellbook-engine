"""Base class for SpellBlocks."""

import logging
from typing import Any

from jinja2 import Template

logger = logging.getLogger(__name__)


class BaseSpellBlock:
    """
    Base class for all SpellBlocks.

    SpellBlocks are reusable components that combine Python logic
    with Jinja2 templates to render HTML content.
    """

    def __init__(self, content: str = "", template: Template | None = None, **kwargs: Any) -> None:
        """
        Initialize a SpellBlock.

        Args:
            content: The inner content of the SpellBlock (between {~ ~} tags)
            template: Jinja2 template for rendering
            **kwargs: Additional arguments passed from the SpellBlock declaration
        """
        self.content = content
        self.template = template
        self.kwargs = kwargs

    def get_context(self) -> dict[str, Any]:
        """
        Get the context dictionary for template rendering.

        Override this method in subclasses to provide custom context.

        Returns:
            Dictionary of variables to pass to the template
        """
        return {"content": self.process_content(), **self.kwargs}

    def process_content(self) -> str:
        """
        Process the inner content of the SpellBlock.

        By default, converts markdown to HTML.
        Override this method to customize content processing.

        Returns:
            Processed content string (HTML)
        """
        if not self.content:
            return ""

        # Import here to avoid circular dependency
        import markdown

        # Process with basic extensions
        # Use a minimal set to avoid full <p> wrapping for inline content
        return markdown.markdown(
            self.content.strip(),
            extensions=[
                "markdown.extensions.fenced_code",
                "markdown.extensions.nl2br",
            ],
        ).strip()

    def process(self, content: str) -> "BaseSpellBlock":
        """
        Process method for compatibility with pipeline processing.

        Args:
            content: Content to process

        Returns:
            Self for chaining
        """
        self.content = content
        return self

    def render(self) -> str:
        """
        Render the SpellBlock to HTML using its template.

        Returns:
            Rendered HTML string
        """
        if not self.template:
            logger.warning(f"No template provided for {self.__class__.__name__}")
            return self.process_content()

        try:
            context = self.get_context()
            rendered: str = self.template.render(**context)
            return rendered
        except Exception as e:
            logger.error(f"Error rendering {self.__class__.__name__}: {e}")
            return f"<!-- Error rendering block: {e} -->"

    def __str__(self) -> str:
        """String representation returns rendered content."""
        return self.render()
