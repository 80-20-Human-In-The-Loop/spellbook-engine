"""Core markdown parser for Spellbook Engine."""

import logging
import re
from typing import Any

import markdown

from .exceptions import ParserError
from .registry import SpellBlockRegistry

logger = logging.getLogger(__name__)


class SpellbookParser:
    """
    Main parser for processing markdown with embedded SpellBlocks.

    This parser:
    1. Protects code blocks from processing
    2. Finds and renders SpellBlocks ({~ block ~}...{~~})
    3. Applies markdown processing with extensions
    """

    # Regex patterns for SpellBlocks
    SPELLBLOCK_PATTERN = re.compile(
        r"{~\s*(\w+)\s*([^~]*?)\s*~}(.*?)(?:{~~})", re.DOTALL | re.IGNORECASE
    )
    SPELLBLOCK_SELF_CLOSING_PATTERN = re.compile(
        r"{~\s*(\w+)\s*([^~]*?)\s*/~}", re.DOTALL | re.IGNORECASE
    )
    CODE_FENCE_PATTERN = re.compile(r"^```", re.MULTILINE)

    def __init__(
        self,
        registry: SpellBlockRegistry | None = None,
        markdown_extensions: list[Any] | None = None,
    ):
        """
        Initialize the parser.

        Args:
            registry: SpellBlockRegistry for managing SpellBlocks
            markdown_extensions: List of markdown extension names or instances
        """
        self.registry = registry or SpellBlockRegistry()

        if markdown_extensions is None:
            self.markdown_extensions = [
                "markdown.extensions.fenced_code",
                "markdown.extensions.tables",
                "markdown.extensions.nl2br",
                "markdown.extensions.sane_lists",
                "markdown.extensions.footnotes",
                "markdown.extensions.attr_list",
                "markdown.extensions.toc",
                "markdown.extensions.extra",
            ]
        else:
            self.markdown_extensions = markdown_extensions

    def render(self, markdown_text: str) -> str:
        """
        Parse and render markdown text with SpellBlocks to HTML.

        Args:
            markdown_text: The markdown text to process

        Returns:
            Rendered HTML string
        """
        try:
            # Split content by code fences to protect them
            segments: list[tuple[str, bool]] = self._split_by_code_fences(markdown_text)

            # Process each segment
            processed_segments = []
            for content, is_code_block in segments:
                if is_code_block:
                    processed_segments.append(content)
                else:
                    processed = self._process_spellblocks(content)
                    processed_segments.append(processed)

            # Join processed segments
            processed_markdown = "".join(processed_segments)

            # Apply markdown processing
            html = markdown.markdown(processed_markdown, extensions=self.markdown_extensions)

            return html

        except Exception as e:
            logger.error(f"Parser error: {e}")
            raise ParserError(f"Failed to parse markdown: {e}") from e

    def _split_by_code_fences(self, text: str) -> list[tuple[str, bool]]:
        """
        Split markdown text into code and non-code segments.

        Args:
            text: The markdown text to split

        Returns:
            List of (segment_text, is_code_block) tuples
        """
        segments = []
        lines = text.splitlines(keepends=True)
        in_code_block = False
        current_segment: list[str] = []
        for line in lines:
            if self.CODE_FENCE_PATTERN.match(line.strip()):
                # Save current segment
                if current_segment:
                    segments.append(("".join(current_segment), in_code_block))
                    current_segment = []
                # Toggle code block state
                in_code_block = not in_code_block
                current_segment.append(line)
            else:
                current_segment.append(line)

        # Add final segment
        if current_segment:
            segments.append(("".join(current_segment), in_code_block))

        return segments

    def _process_spellblocks(self, text: str) -> str:
        """
        Find and process all SpellBlocks in the text.

        Args:
            text: Text segment to process

        Returns:
            Text with SpellBlocks replaced by rendered HTML
        """
        # Check for malformed blocks first
        text = self._detect_malformed_blocks(text)

        # Process self-closing blocks first
        text = self._process_self_closing_blocks(text)

        # Process content-wrapping blocks
        text = self._process_content_blocks(text)

        return text

    def _detect_malformed_blocks(self, text: str) -> str:
        """
        Detect and handle malformed SpellBlocks.

        Looks for:
        - Unclosed opening tags: {~ blockname ~} without matching {~~}
        - Mismatched closing tags: {~ alert ~} ... {~ card ~}
        - Orphaned closing tags: {~~} without opening

        Args:
            text: Text to check for malformed blocks

        Returns:
            Text with malformed blocks replaced by error blocks
        """
        # Pattern to find opening tags
        opening_pattern = re.compile(r"{~\s*(\w+)\s*([^~]*?)\s*~}")
        # Pattern to find closing tags
        closing_pattern = re.compile(r"{~~}")
        # Pattern to find self-closing tags (these are fine)
        self_closing_pattern = re.compile(r"{~\s*(\w+)\s*([^~]*?)\s*/~}")

        # Track positions of tags
        tags: list[tuple[str, int, int, str]] = []  # (type, start, end, name)

        # Find all self-closing tags first and mark them to skip
        self_closing_positions = set()
        for match in self_closing_pattern.finditer(text):
            self_closing_positions.add((match.start(), match.end()))

        # Find all opening tags
        for match in opening_pattern.finditer(text):
            # Skip if this is actually part of a self-closing tag
            if any(
                match.start() >= start and match.end() <= end
                for start, end in self_closing_positions
            ):
                continue
            block_name = match.group(1)
            tags.append(("open", match.start(), match.end(), block_name))

        # Find all closing tags
        for match in closing_pattern.finditer(text):
            tags.append(("close", match.start(), match.end(), ""))

        # Sort by position
        tags.sort(key=lambda x: x[1])

        # Match opening and closing tags
        stack: list[tuple[str, int, int, str]] = []
        replacements: list[tuple[int, int, str]] = []

        for tag_type, start, end, name in tags:
            if tag_type == "open":
                stack.append((tag_type, start, end, name))
            elif tag_type == "close":
                if not stack:
                    # Orphaned closing tag - render error block
                    error_msg = self._render_error(
                        error_type="orphaned_closing",
                        message="Found a closing tag {~~} without a matching opening tag.",
                    )
                    replacements.append((start, end, error_msg))
                else:
                    # Pop the matching opening tag
                    stack.pop()

        # Any remaining items in stack are unclosed tags
        for _tag_type, _start, end, name in stack:
            # Unclosed tag - render error block
            error_msg = self._render_error(
                error_type="unclosed_block",
                block_name=name,
            )
            # Insert error block right after the unclosed tag
            replacements.append((end, end, error_msg))

        # Apply replacements in reverse order to preserve positions
        replacements.sort(key=lambda x: x[0], reverse=True)
        result = text
        for start, end, replacement in replacements:
            if start == end:
                # Insert only
                result = result[:start] + replacement + result[end:]
            else:
                # Replace
                result = result[:start] + replacement + result[end:]

        return result

    def _process_self_closing_blocks(self, text: str) -> str:
        """Process self-closing SpellBlocks ({~ block /~})."""

        def replace_block(match: re.Match[str]) -> str:
            block_name = match.group(1)
            args_str = match.group(2) or ""
            return self._render_spellblock(block_name, args_str, "", True)

        return self.SPELLBLOCK_SELF_CLOSING_PATTERN.sub(replace_block, text)

    def _process_content_blocks(self, text: str) -> str:
        """Process content-wrapping SpellBlocks ({~ block ~}...{~~})."""
        last_match_end = 0
        segments = []

        for match in self.SPELLBLOCK_PATTERN.finditer(text):
            # Add text before this block
            segments.append(text[last_match_end : match.start()])

            # Process the block
            block_name = match.group(1)
            args_str = match.group(2) or ""
            content = match.group(3) or ""

            rendered = self._render_spellblock(block_name, args_str, content, False)
            segments.append(rendered)

            last_match_end = match.end()

        # Add remaining text
        segments.append(text[last_match_end:])

        return "".join(segments)

    def _render_spellblock(
        self, block_name: str, args_str: str, content: str, is_self_closing: bool
    ) -> str:
        """
        Render a single SpellBlock.

        Args:
            block_name: Name of the SpellBlock
            args_str: Argument string from the tag
            content: Inner content (empty for self-closing blocks)
            is_self_closing: Whether this is a self-closing block

        Returns:
            Rendered HTML or error block
        """
        try:
            # Parse arguments
            kwargs = self._parse_arguments(args_str)

            # Recursively process nested SpellBlocks in content
            if content and not is_self_closing:
                content = self._process_spellblocks(content)

            # Get the block from registry
            block = self.registry.create_block(
                block_name, content="" if is_self_closing else content, **kwargs
            )

            if not block:
                logger.warning(f"SpellBlock '{block_name}' not found")
                return self._render_error(
                    error_type="block_not_found",
                    block_name=block_name,
                )

            # Render the block
            rendered = block.render()

            # Clean up the rendered HTML
            if rendered.strip():
                # Ensure proper spacing around block-level elements
                return f"\n\n{rendered.strip()}\n\n"
            return ""

        except Exception as e:
            logger.error(f"Error rendering SpellBlock '{block_name}': {e}")
            return self._render_error(
                error_type="render_exception",
                block_name=block_name,
                content=str(e),
            )

    def _render_error(
        self,
        error_type: str,
        block_name: str = "",
        message: str = "",
        suggestion: str = "",
        content: str = "",
    ) -> str:
        """
        Render an error using the RenderErrorBlock.

        Args:
            error_type: Type of error (unclosed_block, block_not_found, etc.)
            block_name: Name of the SpellBlock that caused the error
            message: Custom error message (optional)
            suggestion: Custom suggestion (optional)
            content: Additional context or technical details (optional)

        Returns:
            Rendered error HTML
        """
        error_block = self.registry.create_block(
            "render_error",
            content=content,
            error_type=error_type,
            block_name=block_name,
            message=message,
            suggestion=suggestion,
        )

        if error_block:
            return f"\n\n{error_block.render().strip()}\n\n"

        # Fallback if render_error block itself isn't available
        return f"<!-- Error: {error_type} for '{block_name}' -->"

    def _parse_arguments(self, args_str: str) -> dict[str, Any]:
        """
        Parse SpellBlock arguments from string.

        Handles: key="value", key='value', key=value, flag

        Args:
            args_str: The argument string to parse

        Returns:
            Dictionary of parsed arguments
        """
        if not args_str or not args_str.strip():
            return {}

        kwargs = {}
        # Pattern for key=value pairs and flags
        pattern = re.compile(
            r"""
            (?P<key>[a-zA-Z_][\w-]*)  # Key name
            (?:                        # Optional value part
                \s*=\s*                # Equals with optional whitespace
                (?:
                    "(?P<dquoted>[^"]*)" |  # Double-quoted value
                    '(?P<squoted>[^']*)' |  # Single-quoted value
                    (?P<unquoted>[^\s"'=<>`]+)  # Unquoted value
                )
            )?
            """,
            re.VERBOSE,
        )

        for match in pattern.finditer(args_str):
            key = match.group("key")

            # Check which value group matched
            if match.group("dquoted") is not None:
                kwargs[key] = match.group("dquoted")
            elif match.group("squoted") is not None:
                kwargs[key] = match.group("squoted")
            elif match.group("unquoted") is not None:
                kwargs[key] = match.group("unquoted")
            else:
                # No value means it's a flag
                kwargs[key] = True

        return kwargs
