"""Custom exceptions for Spellbook Engine with helpful error messages."""

from pathlib import Path


class SpellbookError(Exception):
    """Base exception for all Spellbook Engine errors."""

    pass


class SpellBlockDiscoveryError(SpellbookError):
    """Raised when SpellBlocks cannot be discovered or loaded."""

    def __init__(self, attempted_path: Path | None = None):
        if attempted_path is None:
            message = """
No SpellBlocks directory found. Please provide SpellBlocks using one of:

1. Create a 'spellblocks' folder in your current directory
2. Pass a path: SpellBlockRegistry('path/to/blocks')
3. Pass a config dict: SpellBlockRegistry({'block_name': {...}})

Expected folder structure:
spellblocks/
├── templates/
│   └── your_block.html
└── logic/
    └── your_block.py

Or flat structure:
spellblocks/
├── your_block.html
└── your_block.py
"""
        else:
            message = f"""
Invalid SpellBlocks directory structure at: {attempted_path}

Expected one of:
1. Standard structure:
   {attempted_path}/templates/ and {attempted_path}/logic/

2. Flat structure:
   {attempted_path}/ containing .html and .py files

Found:
{self._list_directory_contents(attempted_path)}
"""
        super().__init__(message)

    def _list_directory_contents(self, path: Path) -> str:
        """Helper to list directory contents for error message."""
        if not path.exists():
            return "  Directory does not exist"

        if not path.is_dir():
            return "  Path is not a directory"

        contents = []
        for item in sorted(path.iterdir())[:10]:  # Limit to first 10 items
            if item.is_dir():
                contents.append(f"  {item.name}/")
            else:
                contents.append(f"  {item.name}")

        if len(list(path.iterdir())) > 10:
            contents.append("  ... and more")

        return "\n".join(contents) if contents else "  Directory is empty"


class SpellBlockLoadError(SpellbookError):
    """Raised when a specific SpellBlock cannot be loaded."""

    def __init__(self, block_name: str, reason: str):
        message = f"""
Failed to load SpellBlock '{block_name}': {reason}

Please check:
1. The logic file exists and has a class named '{block_name.capitalize()}Block'
2. The template file exists and is valid HTML/Jinja2
3. The Python file has no syntax errors
"""
        super().__init__(message)


class SpellBlockRenderError(SpellbookError):
    """Raised when a SpellBlock fails to render."""

    def __init__(self, block_name: str, reason: str):
        message = f"Failed to render SpellBlock '{block_name}': {reason}"
        super().__init__(message)


class ParserError(SpellbookError):
    """Raised when the markdown parser encounters an error."""

    pass
