"""Quote SpellBlock implementation."""

from typing import Any

from spellbook_engine import BaseSpellBlock


class QuoteBlock(BaseSpellBlock):
    """
    Quote SpellBlock for displaying blockquotes with attribution.

    Attributes:
        author: Quote attribution
        source: Source of the quote (book, article, etc.)
        cite: URL citation
    """

    def get_context(self) -> dict[str, Any]:
        """Prepare context for the quote template."""
        return {
            "author": self.kwargs.get("author", ""),
            "source": self.kwargs.get("source", ""),
            "cite": self.kwargs.get("cite", ""),
            "content": self.process_content(),
            "style": self.kwargs.get("style", "default"),  # default, italic, large
        }

    def process_content(self) -> str:
        """Process the quote content (markdown processing handled by base class)."""
        # Base class now handles markdown processing
        return super().process_content()
