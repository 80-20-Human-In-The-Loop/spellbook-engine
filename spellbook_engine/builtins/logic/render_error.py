"""RenderError SpellBlock implementation for compassionate error display."""

from typing import Any

from spellbook_engine import BaseSpellBlock


class RenderErrorBlock(BaseSpellBlock):
    """
    RenderError SpellBlock for displaying helpful, educational error messages.

    This block is used internally by the parser to render errors in a
    compassionate and guidance-oriented way.

    Attributes:
        error_type: Type of error (unclosed_block, orphaned_closing, etc.)
        block_name: Name of the SpellBlock that caused the error
        message: Human-readable error explanation
        suggestion: Specific guidance on how to fix the error
        docs_link: URL to relevant documentation
    """

    def get_context(self) -> dict[str, Any]:
        """Prepare context for the render_error template."""
        error_type = self.kwargs.get("error_type", "unknown")
        block_name = self.kwargs.get("block_name", "")

        # Generate helpful messages based on error type
        error_messages = {
            "unclosed_block": {
                "title": "Unclosed SpellBlock",
                "message": f"The SpellBlock '{block_name}' is missing its closing tag.",
                "suggestion": (
                    f"Add <code>&#123;~~&#125;</code> after your content "
                    f"to close the '{block_name}' block."
                ),
                "icon": "⚠️",
            },
            "orphaned_closing": {
                "title": "Orphaned Closing Tag",
                "message": (
                    "Found a closing tag <code>&#123;~~&#125;</code> "
                    "without a matching opening tag."
                ),
                "suggestion": (
                    "Remove the extra <code>&#123;~~&#125;</code> "
                    "or add the missing opening tag."
                ),
                "icon": "⚠️",
            },
            "block_not_found": {
                "title": "SpellBlock Not Found",
                "message": f"The SpellBlock '{block_name}' doesn't exist in your registry.",
                "suggestion": (
                    f"Check the spelling of '{block_name}' or register "
                    "this block in your SpellBlockRegistry."
                ),
                "icon": "❓",
            },
            "render_exception": {
                "title": "Rendering Error",
                "message": f"An error occurred while rendering '{block_name}'.",
                "suggestion": (
                    "Check the template and logic for syntax errors or missing variables."
                ),
                "icon": "❌",
            },
        }

        error_info = error_messages.get(
            error_type,
            {
                "title": "Unknown Error",
                "message": "An unexpected error occurred.",
                "suggestion": "Please check your SpellBlock syntax.",
                "icon": "⚠️",
            },
        )

        # Allow custom message and suggestion to override defaults
        custom_message = self.kwargs.get("message", "")
        custom_suggestion = self.kwargs.get("suggestion", "")

        return {
            "error_type": error_type,
            "block_name": block_name,
            "title": error_info["title"],
            "message": custom_message or error_info["message"],
            "suggestion": custom_suggestion or error_info["suggestion"],
            "icon": error_info["icon"],
            "docs_link": self.kwargs.get("docs_link", "https://docs.example.com/spellblocks"),
            "content": self.process_content() if self.content else "",
        }

    def process_content(self) -> str:
        """Process error content without markdown processing."""
        # Don't process markdown for error content - keep it plain
        return self.content.strip() if self.content else ""
