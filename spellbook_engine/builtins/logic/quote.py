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

    def get_styles(self) -> str:
        """Return CSS styles for quote block."""
        return """
.sb-quote {
    margin: 20px 0;
    padding: 16px 20px;
    border-left: 4px solid var(--primary-color, #3b82f6);
    background-color: var(--surface-color, #f9fafb);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    color: var(--text-color, #374151);
    transition: background-color 0.2s ease, border-left-color 0.2s ease,
        padding-left 0.2s ease, box-shadow 0.2s ease;
}

.sb-quote:hover {
    background-color: var(--subtle-color, #f3f4f6);
    border-left-color: color-mix(in srgb, var(--primary-color, #3b82f6) 80%, black);
    padding-left: 24px;
    box-shadow: 0 2px 8px color-mix(in srgb, var(--primary-color, #3b82f6) 15%, transparent);
}

.sb-quote-content {
    font-style: italic;
    font-size: 1.05em;
    line-height: 1.6;
    margin: 0;
    color: var(--text-color, #374151);
}

.sb-quote-footer {
    margin-top: 12px;
    font-size: 0.9em;
    color: var(--text-secondary-color, #6b7280);
}

.sb-quote-author {
    font-style: normal;
    font-weight: 500;
    color: var(--text-color, #374151);
}

.sb-quote-source {
    font-style: normal;
    color: var(--text-secondary-color, #6b7280);
}

.sb-quote-default {
    /* Default styling already applied to base .sb-quote */
}

.sb-quote-italic .sb-quote-content {
    font-style: italic;
    font-weight: 300;
}

.sb-quote-large {
    padding: 24px 28px;
}

.sb-quote-large .sb-quote-content {
    font-size: 1.25em;
    line-height: 1.7;
}

.sb-quote-large .sb-quote-footer {
    margin-top: 16px;
    font-size: 1em;
}
"""

    def get_style_priority(self) -> int:
        """Built-in blocks have priority 0."""
        return 0
