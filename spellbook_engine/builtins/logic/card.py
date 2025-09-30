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

    def get_styles(self) -> str:
        """Return CSS styles for card block."""
        return """
.sb-card {
    border: 2px solid var(--subtle-color, #e5e7eb);
    border-radius: 12px;
    margin: 16px 0;
    background-color: var(--surface-color, #f9fafb);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
    overflow: hidden;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    transition: box-shadow 0.3s ease, transform 0.3s ease, border-color 0.3s ease;
}

.sb-card:hover {
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.12);
    transform: translateY(-4px);
    border-color: var(--primary-color, #3b82f6);
}

.sb-card-header {
    position: relative;
    padding: 16px 20px;
    background-color: var(--background-color, #ffffff);
    border-bottom: 2px solid var(--subtle-color, #e5e7eb);
    font-weight: 600;
    font-size: 1.1em;
    color: var(--text-color, #1f2937);
}

.sb-card-header-collapsible {
    cursor: pointer;
    transition: background-color 0.2s ease;
    user-select: none;
}

.sb-card-header-collapsible:hover {
    background-color: color-mix(in srgb, var(--primary-color, #3b82f6) 5%, transparent);
}

.sb-card-body {
    padding: 20px;
    transition: max-height 0.3s ease, padding 0.3s ease, opacity 0.3s ease;
    color: var(--text-color, #1f2937);
}

.sb-card-body.collapsed {
    max-height: 0;
    padding: 0 20px;
    overflow: hidden;
    opacity: 0;
}

.sb-card-footer {
    padding: 12px 20px;
    background-color: var(--background-color, #ffffff);
    border-top: 2px solid var(--subtle-color, #e5e7eb);
    font-size: 0.9em;
    color: var(--text-secondary-color, #6b7280);
}

.sb-card-collapse-btn {
    position: absolute;
    right: 16px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 0.9em;
    color: var(--text-secondary-color, #6b7280);
    pointer-events: none;
    transition: color 0.2s ease;
}

.sb-card-header-collapsible:hover .sb-card-collapse-btn {
    color: var(--primary-color, #3b82f6);
}

.sb-card-collapse-btn span {
    display: inline-block;
    transition: transform 0.3s ease;
}

.sb-card-collapse-btn span.rotated {
    transform: rotate(-90deg);
}

.sb-card-primary {
    border-color: var(--primary-color, #3b82f6);
}

.sb-card-primary .sb-card-header {
    background: linear-gradient(
        135deg,
        var(--primary-color, #3b82f6),
        color-mix(in srgb, var(--primary-color, #3b82f6) 80%, black)
    );
    color: #ffffff;
    border-bottom-color: var(--primary-color, #3b82f6);
}

.sb-card-primary:hover {
    border-color: color-mix(in srgb, var(--primary-color, #3b82f6) 80%, black);
}

.sb-card-secondary {
    border-color: var(--secondary-color, #6b7280);
}

.sb-card-secondary .sb-card-header {
    background: linear-gradient(
        135deg,
        var(--secondary-color, #6b7280),
        color-mix(in srgb, var(--secondary-color, #6b7280) 80%, black)
    );
    color: #ffffff;
    border-bottom-color: var(--secondary-color, #6b7280);
}

.sb-card-secondary:hover {
    border-color: color-mix(in srgb, var(--secondary-color, #6b7280) 80%, black);
}

.sb-card-accent {
    border-color: var(--accent-color, #f59e0b);
}

.sb-card-accent .sb-card-header {
    background: linear-gradient(
        135deg,
        var(--accent-color, #f59e0b),
        color-mix(in srgb, var(--accent-color, #f59e0b) 80%, black)
    );
    color: #ffffff;
    border-bottom-color: var(--accent-color, #f59e0b);
}

.sb-card-accent:hover {
    border-color: color-mix(in srgb, var(--accent-color, #f59e0b) 80%, black);
}

.sb-card-default {
    /* Default styling already applied to base .sb-card */
}
"""

    def get_style_priority(self) -> int:
        """Built-in blocks have priority 0."""
        return 0
