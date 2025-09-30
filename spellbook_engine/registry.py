"""SpellBlock Registry with flexible discovery system."""

import importlib.resources
import importlib.util
import logging
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

from jinja2 import ChoiceLoader, Environment, FileSystemLoader, Template

from .base_block import BaseSpellBlock
from .exceptions import SpellBlockDiscoveryError, SpellBlockLoadError

logger = logging.getLogger(__name__)


class SpellBlockRegistry:
    """
    Registry for SpellBlocks with flexible discovery system.

    Can load SpellBlocks from:
    1. Default 'spellblocks' directory
    2. Custom path with standard or flat structure
    3. Manual dictionary configuration
    """

    def __init__(
        self,
        source: str | Path | dict[str, Any] | None = None,
        load_builtins: bool = True,
    ):
        """
        Initialize the SpellBlock registry.

        Args:
            source: Can be:
                - None: Look for ./spellblocks/ directory (after loading builtins)
                - str/Path: Path to directory containing SpellBlocks
                - dict: Manual config with 'block_name': {'logic_file': ..., 'template_file': ...}
            load_builtins: Whether to load built-in SpellBlocks (default True)
        """
        self._blocks: dict[str, dict[str, Any]] = {}
        self._jinja_env: Environment | None = None
        self._template_dirs: list[Path] = []

        # Load built-in SpellBlocks first
        if load_builtins:
            self._load_builtins()

        # Then load user-provided SpellBlocks (which can override builtins)
        self._discover_and_load(source)

        # Setup Jinja environment with all template directories
        self._setup_jinja_env()

    def _load_builtins(self) -> None:
        """Load built-in SpellBlocks from the package."""
        try:
            # Get path to builtins directory
            import spellbook_engine

            package_dir = Path(spellbook_engine.__file__).parent
            builtins_dir = package_dir / "builtins"

            if builtins_dir.exists():
                templates_dir = builtins_dir / "templates"
                logic_dir = builtins_dir / "logic"

                if templates_dir.exists() and logic_dir.exists():
                    self._template_dirs.append(templates_dir)
                    self._load_standard_structure(templates_dir, logic_dir, is_builtin=True)
                    logger.info("Loaded built-in SpellBlocks")
        except Exception as e:
            logger.warning(f"Could not load built-in SpellBlocks: {e}")

    def _setup_jinja_env(self) -> None:
        """Setup Jinja environment with all collected template directories."""
        if self._template_dirs:
            # Use ChoiceLoader to search multiple directories
            # Reverse order so user templates override built-ins
            loaders = [FileSystemLoader(str(d)) for d in reversed(self._template_dirs)]
            self._jinja_env = Environment(loader=ChoiceLoader(loaders))

    def _discover_and_load(self, source: str | Path | dict[str, Any] | None) -> None:
        """Discover and load SpellBlocks based on the source type."""
        if source is None:
            # Look for default spellblocks directory
            default_path = Path.cwd() / "spellblocks"
            if default_path.exists():
                self._load_from_path(default_path)
            # If no user spellblocks found, that's OK - we have builtins

        elif isinstance(source, str | Path):
            # Load from specified path
            path = Path(source)
            if not path.exists():
                raise SpellBlockDiscoveryError(path)
            self._load_from_path(path)

        elif isinstance(source, dict):
            # Manual configuration
            self._load_from_dict(source)

        else:
            raise ValueError(f"Invalid source type: {type(source)}")

    def _load_from_path(self, path: Path) -> None:
        """Load SpellBlocks from a directory path."""
        if not path.is_dir():
            raise SpellBlockDiscoveryError(path)

        # Check for standard structure (templates/ and logic/)
        templates_dir = path / "templates"
        logic_dir = path / "logic"

        if templates_dir.exists() and logic_dir.exists():
            self._load_standard_structure(templates_dir, logic_dir)
        else:
            # Check for flat structure
            self._load_flat_structure(path)

    def _load_standard_structure(
        self, templates_dir: Path, logic_dir: Path, is_builtin: bool = False
    ) -> None:
        """Load SpellBlocks from standard directory structure."""
        if not is_builtin:
            self._template_dirs.append(templates_dir)

        # Find all template files
        for template_file in templates_dir.glob("*.html"):
            block_name = template_file.stem
            logic_file = logic_dir / f"{block_name}.py"

            if logic_file.exists():
                self._register_block(block_name, logic_file=logic_file, template_file=template_file)
            else:
                logger.warning(f"No logic file found for template: {template_file}")

    def _load_flat_structure(self, path: Path) -> None:
        """Load SpellBlocks from flat directory structure."""
        self._template_dirs.append(path)

        # Find pairs of .html and .py files
        html_files = {f.stem: f for f in path.glob("*.html")}
        py_files = {f.stem: f for f in path.glob("*.py")}

        if not html_files and not py_files:
            raise SpellBlockDiscoveryError(path)

        # Match pairs
        for block_name in html_files.keys() & py_files.keys():
            self._register_block(
                block_name,
                logic_file=py_files[block_name],
                template_file=html_files[block_name],
            )

    def _load_from_dict(self, config: dict[str, Any]) -> None:
        """Load SpellBlocks from manual dictionary configuration."""
        # Check for special _discover_path key for hybrid approach
        if "_discover_path" in config:
            discover_path = Path(config.pop("_discover_path"))
            self._load_from_path(discover_path)

        # Process manual entries
        for block_name, block_config in config.items():
            if not isinstance(block_config, dict):
                raise ValueError(f"Invalid configuration for block '{block_name}'")

            logic_file = block_config.get("logic_file")
            template_file = block_config.get("template_file")

            if not logic_file or not template_file:
                raise ValueError(
                    f"Block '{block_name}' must have both 'logic_file' and 'template_file'"
                )

            self._register_block(
                block_name,
                logic_file=Path(logic_file),
                template_file=Path(template_file),
            )

        # Collect unique template directories from manual entries
        for block_info in self._blocks.values():
            template_dir = block_info["template_file"].parent
            if template_dir not in self._template_dirs:
                self._template_dirs.append(template_dir)

    def _register_block(self, block_name: str, logic_file: Path, template_file: Path) -> None:
        """Register a single SpellBlock."""
        try:
            # Load the logic module
            module = self._load_python_module(block_name, logic_file)

            # Find the block class (looking for NameBlock or name_block pattern)
            block_class = None
            class_name = f"{block_name.capitalize()}Block"

            if hasattr(module, class_name):
                block_class = getattr(module, class_name)
            else:
                # Try to find any class that inherits from BaseSpellBlock
                for _name, obj in vars(module).items():
                    if (
                        isinstance(obj, type)
                        and issubclass(obj, BaseSpellBlock)
                        and obj is not BaseSpellBlock
                    ):
                        block_class = obj
                        break

            if not block_class:
                raise SpellBlockLoadError(
                    block_name, f"No suitable block class found in {logic_file}"
                )

            # Store registration info
            self._blocks[block_name] = {
                "class": block_class,
                "template_file": template_file,
                "template_name": template_file.name,
            }

            logger.info(f"Registered SpellBlock: {block_name}")

        except Exception as e:
            raise SpellBlockLoadError(block_name, str(e)) from e

    def _load_python_module(self, name: str, file_path: Path) -> ModuleType:
        """Dynamically load a Python module from file."""
        module_name = f"spellblock_{name}"
        spec = importlib.util.spec_from_file_location(module_name, file_path)

        if not spec or not spec.loader:
            raise ImportError(f"Cannot load module from {file_path}")

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        return module

    def get_block(self, name: str) -> type[BaseSpellBlock] | None:
        """Get a registered SpellBlock class by name."""
        block_info = self._blocks.get(name)
        if block_info:
            block_class: type[BaseSpellBlock] = block_info["class"]
            return block_class
        return None

    def get_template(self, name: str) -> Template | None:
        """Get a Jinja2 template for a SpellBlock."""
        if not self._jinja_env:
            return None

        block_info = self._blocks.get(name)
        if block_info:
            return self._jinja_env.get_template(block_info["template_name"])
        return None

    def list_blocks(self) -> list[str]:
        """List all registered SpellBlock names."""
        return list(self._blocks.keys())

    def create_block(self, name: str, content: str = "", **kwargs: Any) -> BaseSpellBlock | None:
        """Create an instance of a SpellBlock."""
        block_class = self.get_block(name)
        if not block_class:
            return None

        template = self.get_template(name)
        if not template:
            return None

        return block_class(content=content, template=template, **kwargs)
