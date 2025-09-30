"""Style management system for Spellbook Engine."""

import hashlib
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from .theme import Theme


class StyleSheet(BaseModel):
    """
    Represents a CSS stylesheet with metadata.

    Attributes:
        block_name: Name of the SpellBlock this style belongs to
        css: The CSS content as a string
        priority: Priority for ordering (0=builtins, 10=user, 20=inline)
        hash: MD5 hash of CSS content for deduplication
    """

    block_name: str
    css: str
    priority: int = Field(default=10)
    hash: str = Field(default="")

    def model_post_init(self, __context: Any) -> None:
        """Calculate hash after initialization."""
        if not self.hash:
            self.hash = hashlib.md5(self.css.encode()).hexdigest()


class StyleRegistry:
    """
    Registry for tracking and deduplicating styles during rendering.

    Keeps track of which styles have been loaded and prevents duplicates.
    """

    def __init__(self) -> None:
        """Initialize the style registry."""
        self._loaded_hashes: set[str] = set()
        self._styles: list[StyleSheet] = []

    def register(self, stylesheet: StyleSheet) -> bool:
        """
        Register a stylesheet if not already loaded.

        Args:
            stylesheet: The StyleSheet to register

        Returns:
            True if stylesheet was registered, False if duplicate
        """
        if stylesheet.hash in self._loaded_hashes:
            return False

        self._loaded_hashes.add(stylesheet.hash)
        self._styles.append(stylesheet)
        return True

    def get_all_styles(self) -> list[StyleSheet]:
        """
        Get all registered styles sorted by priority.

        Returns:
            List of StyleSheets sorted by priority (lowest first)
        """
        return sorted(self._styles, key=lambda s: s.priority)

    def clear(self) -> None:
        """Clear all registered styles."""
        self._loaded_hashes.clear()
        self._styles.clear()


class StyleCollector:
    """
    Collects styles during rendering and outputs grouped <style> tag.

    Supports optional theme injection - when a theme is provided, CSS variables
    will be prepended to the output in a :root {} block.

    Usage:
        collector = StyleCollector()
        # During rendering, add styles
        collector.add_style(block_name="alert", css="...", priority=0)
        # At end, get combined style tag
        style_tag = collector.render()

    With theme:
        from spellbook_engine.theme import Theme
        collector = StyleCollector(theme=my_theme)
        style_tag = collector.render()  # Includes :root { CSS variables }
    """

    def __init__(self, theme: "Theme | None" = None) -> None:
        """
        Initialize the style collector.

        Args:
            theme: Optional Theme object for injecting CSS variables
        """
        self.registry = StyleRegistry()
        self.theme = theme

    def add_style(
        self,
        block_name: str,
        css: str,
        priority: int = 10,
    ) -> bool:
        """
        Add a style to the collector.

        Args:
            block_name: Name of the block
            css: CSS content
            priority: Priority for ordering (0=builtin, 10=user, 20=inline)

        Returns:
            True if style was added, False if duplicate
        """
        stylesheet = StyleSheet(
            block_name=block_name,
            css=css,
            priority=priority,
        )
        return self.registry.register(stylesheet)

    def render(self) -> str:
        """
        Render all collected styles into a single <style> tag.

        If a theme is set, prepends :root {} block with CSS variables.

        Returns:
            HTML <style> tag with all CSS, or empty string if no styles
        """
        styles = self.registry.get_all_styles()
        if not styles and not self.theme:
            return ""

        css_parts = []

        # Add theme CSS variables at the top if theme is set
        if self.theme:
            css_parts.append(self.theme.to_css_root_block())
            css_parts.append("")  # Empty line after :root block

        # Group CSS by block with comments
        for stylesheet in styles:
            css_parts.append(f"/* {stylesheet.block_name} */")
            css_parts.append(stylesheet.css)
            css_parts.append("")  # Empty line between blocks

        combined_css = "\n".join(css_parts)
        return f"<style>\n{combined_css}\n</style>"

    def clear(self) -> None:
        """Clear all collected styles."""
        self.registry.clear()
