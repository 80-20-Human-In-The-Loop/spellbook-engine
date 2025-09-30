"""
Spellbook Engine - A flexible markdown parser with reusable HTML/Python components

Main components:
- SpellbookParser: The main parser for processing markdown with SpellBlocks
- SpellBlockRegistry: Registry for discovering and managing SpellBlocks
"""

from .base_block import BaseSpellBlock
from .parser import SpellbookParser
from .registry import SpellBlockRegistry

__version__ = "0.1.0"
__all__ = ["SpellbookParser", "SpellBlockRegistry", "BaseSpellBlock"]
