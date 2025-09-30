"""Alert SpellBlock implementation."""

from typing import Any

from spellbook_engine import BaseSpellBlock


class AlertBlock(BaseSpellBlock):
    """
    Alert SpellBlock for displaying notification messages.

    Supported types: info, warning, danger, success
    """

    def get_context(self) -> dict[str, Any]:
        """Prepare context for the alert template."""
        alert_type = self.kwargs.get("type", "info")
        dismissible = self.kwargs.get("dismissible", False)

        # Map type to CSS class
        type_classes = {
            "info": "sb-alert-info",
            "warning": "sb-alert-warning",
            "danger": "sb-alert-danger",
            "success": "sb-alert-success",
        }

        return {
            "type": alert_type,
            "css_class": type_classes.get(alert_type, "sb-alert-info"),
            "dismissible": dismissible,
            "content": self.process_content(),
            "title": self.kwargs.get("title", ""),
        }

    def process_content(self) -> str:
        """Process the alert content (markdown processing handled by base class)."""
        # Base class now handles markdown processing
        return super().process_content()

    def get_styles(self) -> str:
        """Return CSS styles for alert block."""
        return """
.sb-alert {
    position: relative;
    padding: 16px 20px;
    margin: 16px 0;
    border: 2px solid;
    border-radius: 8px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    transition: box-shadow 0.2s ease, border-color 0.2s ease;
}

.sb-alert-info {
    background-color: color-mix(in srgb, var(--info-color, #2563eb) 10%, transparent);
    border-color: var(--info-color, #2563eb);
    color: var(--text-color, #1f2937);
}

.sb-alert-info:hover {
    border-color: color-mix(in srgb, var(--info-color, #2563eb) 80%, black);
    box-shadow: 0 2px 8px color-mix(in srgb, var(--info-color, #2563eb) 20%, transparent);
}

.sb-alert-warning {
    background-color: color-mix(in srgb, var(--warning-color, #f59e0b) 10%, transparent);
    border-color: var(--warning-color, #f59e0b);
    color: var(--text-color, #1f2937);
}

.sb-alert-warning:hover {
    border-color: color-mix(in srgb, var(--warning-color, #f59e0b) 80%, black);
    box-shadow: 0 2px 8px color-mix(in srgb, var(--warning-color, #f59e0b) 20%, transparent);
}

.sb-alert-danger {
    background-color: color-mix(in srgb, var(--error-color, #dc2626) 10%, transparent);
    border-color: var(--error-color, #dc2626);
    color: var(--text-color, #1f2937);
}

.sb-alert-danger:hover {
    border-color: color-mix(in srgb, var(--error-color, #dc2626) 80%, black);
    box-shadow: 0 2px 8px color-mix(in srgb, var(--error-color, #dc2626) 20%, transparent);
}

.sb-alert-success {
    background-color: color-mix(in srgb, var(--success-color, #16a34a) 10%, transparent);
    border-color: var(--success-color, #16a34a);
    color: var(--text-color, #1f2937);
}

.sb-alert-success:hover {
    border-color: color-mix(in srgb, var(--success-color, #16a34a) 80%, black);
    box-shadow: 0 2px 8px color-mix(in srgb, var(--success-color, #16a34a) 20%, transparent);
}

.sb-alert-close {
    position: absolute;
    top: 12px;
    right: 12px;
    background: none;
    border: none;
    font-size: 1.5em;
    line-height: 1;
    cursor: pointer;
    opacity: 0.5;
    padding: 0;
    width: 24px;
    height: 24px;
    color: inherit;
    transition: opacity 0.2s ease, transform 0.2s ease;
}

.sb-alert-close:hover {
    opacity: 1;
    transform: scale(1.1);
}

.sb-alert strong {
    display: block;
    margin-bottom: 4px;
    font-weight: 600;
    color: var(--text-color, #1f2937);
}
"""

    def get_style_priority(self) -> int:
        """Built-in blocks have priority 0."""
        return 0
