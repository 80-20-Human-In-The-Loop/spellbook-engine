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
            "info": "alert-info",
            "warning": "alert-warning",
            "danger": "alert-danger",
            "success": "alert-success",
        }

        return {
            "type": alert_type,
            "css_class": type_classes.get(alert_type, "alert-info"),
            "dismissible": dismissible,
            "content": self.process_content(),
            "title": self.kwargs.get("title", ""),
        }

    def process_content(self) -> str:
        """Process the alert content (markdown processing handled by base class)."""
        # Base class now handles markdown processing
        return super().process_content()
