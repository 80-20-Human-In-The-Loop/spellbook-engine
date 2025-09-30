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

    def get_styles(self) -> str:
        """Return CSS styles for render error block."""
        return """
.sb-render-error {
    border: 2px solid var(--warning-color, #f59e0b);
    border-radius: 8px;
    padding: 16px;
    margin: 16px 0;
    background-color: color-mix(in srgb, var(--warning-color, #f59e0b) 8%, transparent);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.sb-render-error:hover {
    border-color: color-mix(in srgb, var(--warning-color, #f59e0b) 80%, black);
    box-shadow: 0 2px 8px color-mix(in srgb, var(--warning-color, #f59e0b) 20%, transparent);
}

.sb-render-error-unclosed_block {
    border-color: var(--warning-color, #f59e0b);
    background-color: color-mix(in srgb, var(--warning-color, #f59e0b) 8%, transparent);
}

.sb-render-error-unclosed_block:hover {
    border-color: color-mix(in srgb, var(--warning-color, #f59e0b) 80%, black);
}

.sb-render-error-orphaned_closing {
    border-color: var(--warning-color, #f59e0b);
    background-color: color-mix(in srgb, var(--warning-color, #f59e0b) 8%, transparent);
}

.sb-render-error-orphaned_closing:hover {
    border-color: color-mix(in srgb, var(--warning-color, #f59e0b) 80%, black);
}

.sb-render-error-block_not_found {
    border-color: var(--info-color, #3b82f6);
    background-color: color-mix(in srgb, var(--info-color, #3b82f6) 8%, transparent);
}

.sb-render-error-block_not_found:hover {
    border-color: color-mix(in srgb, var(--info-color, #3b82f6) 80%, black);
}

.sb-render-error-render_exception {
    border-color: var(--error-color, #ef4444);
    background-color: color-mix(in srgb, var(--error-color, #ef4444) 8%, transparent);
}

.sb-render-error-render_exception:hover {
    border-color: color-mix(in srgb, var(--error-color, #ef4444) 80%, black);
}

.sb-render-error-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 12px;
}

.sb-render-error-icon {
    font-size: 1.5em;
}

.sb-render-error-title {
    font-size: 1.1em;
    font-weight: 600;
    color: var(--text-color, #1f2937);
}

.sb-render-error-body {
    margin-bottom: 12px;
}

.sb-render-error-message {
    margin: 8px 0;
    color: var(--text-color, #1f2937);
}

.sb-render-error-suggestion {
    background-color: color-mix(in srgb, var(--warning-color, #f59e0b) 15%, transparent);
    border-left: 3px solid var(--warning-color, #f59e0b);
    padding: 10px 12px;
    margin: 12px 0;
    border-radius: 4px;
}

.sb-render-error-details {
    margin: 8px 0;
    font-family: 'Monaco', 'Menlo', 'Courier New', monospace;
    font-size: 0.9em;
    color: var(--text-color, #1f2937);
}

.sb-render-error-details code {
    background-color: color-mix(in srgb, var(--warning-color, #f59e0b) 15%, transparent);
    padding: 2px 6px;
    border-radius: 3px;
}

.sb-render-error-technical {
    margin: 12px 0;
    font-size: 0.9em;
}

.sb-render-error-technical summary {
    cursor: pointer;
    color: var(--text-color, #1f2937);
    font-weight: 500;
    transition: color 0.2s ease;
}

.sb-render-error-technical summary:hover {
    color: var(--primary-color, #3b82f6);
    text-decoration: underline;
}

.sb-render-error-technical pre {
    background-color: color-mix(in srgb, var(--warning-color, #f59e0b) 15%, transparent);
    padding: 8px;
    border-radius: 4px;
    overflow-x: auto;
    margin-top: 8px;
}

.sb-render-error-technical code {
    font-family: 'Monaco', 'Menlo', 'Courier New', monospace;
    font-size: 0.85em;
    color: var(--text-color, #1f2937);
}

.sb-render-error-footer {
    border-top: 1px solid var(--subtle-color, #e5e7eb);
    padding-top: 8px;
    margin-top: 12px;
}

.sb-render-error-docs-link {
    color: var(--primary-color, #3b82f6);
    text-decoration: none;
    font-size: 0.9em;
    font-weight: 500;
    transition: color 0.2s ease;
}

.sb-render-error-docs-link:hover {
    color: color-mix(in srgb, var(--primary-color, #3b82f6) 80%, black);
    text-decoration: underline;
}
"""

    def get_style_priority(self) -> int:
        """Built-in blocks have priority 0."""
        return 0
