"""Card SpellBlock implementation."""

from typing import Any

from spellbook_engine import BaseSpellBlock


class CardBlock(BaseSpellBlock):
    """
    Card SpellBlock for displaying content in a card layout.

    Attributes:
        title: Card header title
        footer: Card footer text
        style: Card style variant (default, primary, secondary, etc.)
    """

    def get_context(self) -> dict[str, Any]:
        """Prepare context for the card template."""
        return {
            "title": self.kwargs.get("title", ""),
            "footer": self.kwargs.get("footer", ""),
            "style": self.kwargs.get("style", "default"),
            "content": self.process_content(),
            "collapsible": self.kwargs.get("collapsible", False),
            "collapsed": self.kwargs.get("collapsed", False),
        }

    def process_content(self) -> str:
        """Process the card content (markdown processing handled by base class)."""
        # Base class now handles markdown processing
        return super().process_content()
