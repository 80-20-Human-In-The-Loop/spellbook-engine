"""Theme system for Spellbook Engine.

Provides a framework-agnostic theming system that's 100% compatible
with Django Spellbook's theme format and CSS variables.
"""

from pydantic import BaseModel, Field, field_validator


class ThemeColors(BaseModel):
    """
    Color palette for a theme.

    All colors should be valid CSS color values (hex, rgb, hsl, etc.).
    Defaults match Django Spellbook's default theme.
    """

    # Core semantic colors
    primary: str = Field(default="#3b82f6", description="Primary brand color")
    secondary: str = Field(default="#6b7280", description="Secondary color")
    accent: str = Field(default="#f59e0b", description="Accent/highlight color")
    neutral: str = Field(default="#2563eb", description="Neutral color for subtle elements")

    # Status colors
    error: str = Field(default="#dc2626", description="Error state color")
    warning: str = Field(default="#f59e0b", description="Warning state color")
    success: str = Field(default="#16a34a", description="Success state color")
    info: str = Field(default="#2563eb", description="Info state color")

    # Extended palette (from Django Spellbook)
    emphasis: str = Field(default="#8b5cf6", description="Emphasis color for special content")
    subtle: str = Field(default="#f3f4f6", description="Subtle background color")
    distinct: str = Field(default="#06b6d4", description="Distinct color for differentiation")
    aether: str = Field(default="#c026d3", description="Magical/mystical theme color")
    artifact: str = Field(default="#a16207", description="Artifact/item theme color")
    sylvan: str = Field(default="#3f6212", description="Nature/sylvan theme color")
    danger: str = Field(default="#a80000", description="Danger/critical state color")

    # System colors
    background: str = Field(default="#ffffff", description="Main background color")
    surface: str = Field(default="#f9fafb", description="Surface/card background color")
    text: str = Field(default="#1f2937", description="Primary text color")
    text_secondary: str = Field(default="#6b7280", description="Secondary text color")

    @field_validator("*")
    @classmethod
    def validate_color(cls, v: str) -> str:
        """Basic validation that color string is not empty."""
        if not v or not isinstance(v, str):
            raise ValueError("Color must be a non-empty string")
        v = v.strip()
        if not v:
            raise ValueError("Color must be a non-empty string")
        return v

    def to_css_variables(self) -> dict[str, str]:
        """
        Convert theme colors to CSS variable format.

        Returns:
            Dict mapping CSS variable names to color values
            Example: {"--primary-color": "#3b82f6", ...}
        """
        css_vars = {}
        for field_name, field_value in self.model_dump().items():
            css_name = field_name.replace("_", "-")
            css_vars[f"--{css_name}-color"] = field_value
        return css_vars


class Theme(BaseModel):
    """
    Complete theme configuration.

    Compatible with Django Spellbook's theme format.
    """

    name: str = Field(description="Theme name")
    colors: ThemeColors = Field(default_factory=ThemeColors, description="Color palette")
    generate_variants: bool = Field(
        default=True,
        description="Generate opacity variants (25%, 50%, 75%) using color-mix()",
    )
    custom_colors: dict[str, str] | None = Field(
        default=None,
        description="Additional custom color variables",
    )

    def to_css_variables(self, include_variants: bool = True) -> dict[str, str]:
        """
        Generate complete CSS variable set from theme.

        Args:
            include_variants: Include opacity variants if generate_variants=True

        Returns:
            Dict mapping CSS variable names to their values/expressions
        """
        css_vars = self.colors.to_css_variables()

        # Add opacity variants if enabled
        if include_variants and self.generate_variants:
            base_colors = self.colors.to_css_variables()
            for var_name, color_value in base_colors.items():
                # Generate 25%, 50%, 75% opacity variants
                for opacity in [25, 50, 75]:
                    variant_name = f"{var_name}-{opacity}"
                    css_vars[variant_name] = (
                        f"color-mix(in srgb, {color_value} {opacity}%, transparent)"
                    )

        # Add custom colors if provided
        if self.custom_colors:
            for name, value in self.custom_colors.items():
                css_name = name if name.startswith("--") else f"--{name}"
                css_vars[css_name] = value

        return css_vars

    def to_css_root_block(self) -> str:
        """
        Generate complete :root {} CSS block with all variables.

        Returns:
            CSS string with :root declaration
        """
        css_vars = self.to_css_variables()
        lines = [":root {"]
        for var_name, var_value in sorted(css_vars.items()):
            lines.append(f"  {var_name}: {var_value};")
        lines.append("}")
        return "\n".join(lines)


# Preset themes matching Django Spellbook
PRESET_THEMES: dict[str, Theme] = {
    "default": Theme(
        name="Default",
        colors=ThemeColors(),
    ),
    "arcane": Theme(
        name="Arcane",
        colors=ThemeColors(
            primary="#8b5cf6",
            secondary="#6b7280",
            accent="#fbbf24",
            neutral="#6366f1",
            error="#ef4444",
            warning="#f59e0b",
            success="#10b981",
            info="#3b82f6",
            emphasis="#a855f7",
            subtle="#f3f4f6",
            distinct="#8b5cf6",
            aether="#c026d3",
            artifact="#d97706",
            sylvan="#059669",
            danger="#dc2626",
            background="#ffffff",
            surface="#faf5ff",
            text="#1f2937",
            text_secondary="#6b7280",
        ),
    ),
    "forest": Theme(
        name="Forest",
        colors=ThemeColors(
            primary="#059669",
            secondary="#6b7280",
            accent="#fbbf24",
            neutral="#10b981",
            error="#dc2626",
            warning="#f59e0b",
            success="#10b981",
            info="#0891b2",
            emphasis="#047857",
            subtle="#f0fdf4",
            distinct="#14b8a6",
            aether="#2dd4bf",
            artifact="#d97706",
            sylvan="#15803d",
            danger="#991b1b",
            background="#ffffff",
            surface="#f0fdf4",
            text="#1f2937",
            text_secondary="#6b7280",
        ),
    ),
    "crimson": Theme(
        name="Crimson",
        colors=ThemeColors(
            primary="#dc2626",
            secondary="#6b7280",
            accent="#fbbf24",
            neutral="#ef4444",
            error="#991b1b",
            warning="#f59e0b",
            success="#10b981",
            info="#3b82f6",
            emphasis="#be123c",
            subtle="#fef2f2",
            distinct="#f43f5e",
            aether="#e11d48",
            artifact="#d97706",
            sylvan="#059669",
            danger="#7f1d1d",
            background="#ffffff",
            surface="#fef2f2",
            text="#1f2937",
            text_secondary="#6b7280",
        ),
    ),
    "ocean": Theme(
        name="Ocean",
        colors=ThemeColors(
            primary="#0891b2",
            secondary="#6b7280",
            accent="#fbbf24",
            neutral="#06b6d4",
            error="#dc2626",
            warning="#f59e0b",
            success="#10b981",
            info="#0284c7",
            emphasis="#0e7490",
            subtle="#ecfeff",
            distinct="#06b6d4",
            aether="#22d3ee",
            artifact="#d97706",
            sylvan="#059669",
            danger="#991b1b",
            background="#ffffff",
            surface="#ecfeff",
            text="#1f2937",
            text_secondary="#6b7280",
        ),
    ),
    "sunset": Theme(
        name="Sunset",
        colors=ThemeColors(
            primary="#f97316",
            secondary="#6b7280",
            accent="#fbbf24",
            neutral="#fb923c",
            error="#dc2626",
            warning="#f59e0b",
            success="#10b981",
            info="#3b82f6",
            emphasis="#ea580c",
            subtle="#fff7ed",
            distinct="#fb923c",
            aether="#f59e0b",
            artifact="#d97706",
            sylvan="#059669",
            danger="#991b1b",
            background="#ffffff",
            surface="#fff7ed",
            text="#1f2937",
            text_secondary="#6b7280",
        ),
    ),
}


def get_preset_theme(name: str) -> Theme | None:
    """
    Get a preset theme by name.

    Args:
        name: Theme name (case-insensitive)

    Returns:
        Theme object or None if not found
    """
    return PRESET_THEMES.get(name.lower())


def list_preset_themes() -> list[str]:
    """
    Get list of available preset theme names.

    Returns:
        List of theme names
    """
    return list(PRESET_THEMES.keys())
