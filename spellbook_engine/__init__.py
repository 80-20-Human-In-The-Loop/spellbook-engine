"""
Spellbook Engine - A flexible markdown parser with reusable HTML/Python components

Main components:
- SpellbookParser: The main parser for processing markdown with SpellBlocks
- SpellBlockRegistry: Registry for discovering and managing SpellBlocks
- Theme: Theme configuration for CSS variables
- ThemeColors: Color palette for themes
"""

from .base_block import BaseSpellBlock
from .parser import SpellbookParser
from .registry import SpellBlockRegistry
from .theme import PRESET_THEMES, Theme, ThemeColors

__version__ = "0.1.0"
__all__ = [
    "SpellbookParser",
    "SpellBlockRegistry",
    "BaseSpellBlock",
    "Theme",
    "ThemeColors",
    "PRESET_THEMES",
]
