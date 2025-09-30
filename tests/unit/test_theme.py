"""Tests for the theme system."""

import pytest

from spellbook_engine import PRESET_THEMES, Theme, ThemeColors
from spellbook_engine.theme import get_preset_theme, list_preset_themes


class TestThemeColors:
    """Test ThemeColors model."""

    def test_default_colors(self):
        """Test ThemeColors with default values."""
        colors = ThemeColors()
        assert colors.primary == "#3b82f6"
        assert colors.secondary == "#6b7280"
        assert colors.accent == "#f59e0b"
        assert colors.error == "#dc2626"
        assert colors.warning == "#f59e0b"
        assert colors.success == "#16a34a"
        assert colors.info == "#2563eb"
        assert colors.background == "#ffffff"
        assert colors.text == "#1f2937"

    def test_custom_colors(self):
        """Test ThemeColors with custom values."""
        colors = ThemeColors(
            primary="#FF6B35",
            accent="#FFD700",
            background="#1a1a1a",
            text="#ffffff",
        )
        assert colors.primary == "#FF6B35"
        assert colors.accent == "#FFD700"
        assert colors.background == "#1a1a1a"
        assert colors.text == "#ffffff"
        # Default values still present
        assert colors.secondary == "#6b7280"

    def test_to_css_variables(self):
        """Test conversion to CSS variables."""
        colors = ThemeColors(primary="#FF6B35", accent="#FFD700")
        css_vars = colors.to_css_variables()

        assert "--primary-color" in css_vars
        assert css_vars["--primary-color"] == "#FF6B35"
        assert "--accent-color" in css_vars
        assert css_vars["--accent-color"] == "#FFD700"
        assert "--text-color" in css_vars
        assert "--text-secondary-color" in css_vars  # Check key exists

    def test_color_validation(self):
        """Test that empty colors are rejected."""
        with pytest.raises(ValueError, match="Color must be a non-empty string"):
            ThemeColors(primary="")

    def test_all_color_fields_present(self):
        """Test that all expected color fields are present."""
        colors = ThemeColors()
        expected_fields = [
            "primary",
            "secondary",
            "accent",
            "neutral",
            "error",
            "warning",
            "success",
            "info",
            "emphasis",
            "subtle",
            "distinct",
            "aether",
            "artifact",
            "sylvan",
            "danger",
            "background",
            "surface",
            "text",
            "text_secondary",
        ]
        for field in expected_fields:
            assert hasattr(colors, field)


class TestTheme:
    """Test Theme model."""

    def test_default_theme(self):
        """Test Theme with default values."""
        theme = Theme(name="Test")
        assert theme.name == "Test"
        assert isinstance(theme.colors, ThemeColors)
        assert theme.generate_variants is True
        assert theme.custom_colors is None

    def test_custom_theme(self):
        """Test Theme with custom colors."""
        colors = ThemeColors(primary="#FF6B35", accent="#FFD700")
        theme = Theme(name="CustomTheme", colors=colors)
        assert theme.name == "CustomTheme"
        assert theme.colors.primary == "#FF6B35"
        assert theme.colors.accent == "#FFD700"

    def test_theme_with_custom_colors_dict(self):
        """Test Theme with additional custom colors."""
        theme = Theme(
            name="Test",
            custom_colors={
                "brand-primary": "#123456",
                "brand-secondary": "#abcdef",
            },
        )
        assert theme.custom_colors == {
            "brand-primary": "#123456",
            "brand-secondary": "#abcdef",
        }

    def test_to_css_variables_without_variants(self):
        """Test CSS variable generation without opacity variants."""
        colors = ThemeColors(primary="#FF6B35")
        theme = Theme(name="Test", colors=colors, generate_variants=False)
        css_vars = theme.to_css_variables()

        # Should have base colors
        assert "--primary-color" in css_vars
        assert css_vars["--primary-color"] == "#FF6B35"

        # Should NOT have opacity variants
        assert "--primary-color-25" not in css_vars
        assert "--primary-color-50" not in css_vars
        assert "--primary-color-75" not in css_vars

    def test_to_css_variables_with_variants(self):
        """Test CSS variable generation with opacity variants."""
        colors = ThemeColors(primary="#FF6B35")
        theme = Theme(name="Test", colors=colors, generate_variants=True)
        css_vars = theme.to_css_variables()

        # Should have base color
        assert "--primary-color" in css_vars
        assert css_vars["--primary-color"] == "#FF6B35"

        # Should have opacity variants
        assert "--primary-color-25" in css_vars
        assert "color-mix(in srgb, #FF6B35 25%, transparent)" in css_vars["--primary-color-25"]
        assert "--primary-color-50" in css_vars
        assert "color-mix(in srgb, #FF6B35 50%, transparent)" in css_vars["--primary-color-50"]
        assert "--primary-color-75" in css_vars
        assert "color-mix(in srgb, #FF6B35 75%, transparent)" in css_vars["--primary-color-75"]

    def test_to_css_variables_includes_custom_colors(self):
        """Test that custom colors are included in CSS variables."""
        theme = Theme(
            name="Test",
            custom_colors={
                "brand-primary": "#123456",
                "--brand-secondary": "#abcdef",  # Test with and without --
            },
        )
        css_vars = theme.to_css_variables()

        assert "--brand-primary" in css_vars
        assert css_vars["--brand-primary"] == "#123456"
        assert "--brand-secondary" in css_vars
        assert css_vars["--brand-secondary"] == "#abcdef"

    def test_to_css_root_block(self):
        """Test CSS :root block generation."""
        colors = ThemeColors(primary="#FF6B35", accent="#FFD700")
        theme = Theme(name="Test", colors=colors, generate_variants=False)
        css_root = theme.to_css_root_block()

        assert css_root.startswith(":root {")
        assert css_root.endswith("}")
        assert "--primary-color: #FF6B35;" in css_root
        assert "--accent-color: #FFD700;" in css_root

    def test_to_css_root_block_with_variants(self):
        """Test CSS :root block includes opacity variants."""
        colors = ThemeColors(primary="#FF6B35")
        theme = Theme(name="Test", colors=colors, generate_variants=True)
        css_root = theme.to_css_root_block()

        assert "--primary-color: #FF6B35;" in css_root
        assert "--primary-color-25:" in css_root
        assert "color-mix(in srgb, #FF6B35 25%, transparent)" in css_root


class TestPresetThemes:
    """Test preset themes."""

    def test_preset_themes_exist(self):
        """Test that preset themes dictionary is populated."""
        assert len(PRESET_THEMES) > 0
        assert "default" in PRESET_THEMES
        assert "arcane" in PRESET_THEMES

    def test_preset_theme_default(self):
        """Test default preset theme."""
        theme = PRESET_THEMES["default"]
        assert theme.name == "Default"
        assert isinstance(theme.colors, ThemeColors)
        assert theme.colors.primary == "#3b82f6"

    def test_preset_theme_arcane(self):
        """Test arcane preset theme."""
        theme = PRESET_THEMES["arcane"]
        assert theme.name == "Arcane"
        assert theme.colors.primary == "#8b5cf6"
        assert theme.colors.accent == "#fbbf24"

    def test_all_preset_themes_valid(self):
        """Test that all preset themes are valid Theme objects."""
        for _name, theme in PRESET_THEMES.items():
            assert isinstance(theme, Theme)
            assert theme.name
            assert isinstance(theme.colors, ThemeColors)

    def test_get_preset_theme(self):
        """Test getting preset theme by name."""
        theme = get_preset_theme("default")
        assert theme is not None
        assert theme.name == "Default"

    def test_get_preset_theme_case_insensitive(self):
        """Test that preset theme lookup is case-insensitive."""
        theme1 = get_preset_theme("arcane")
        theme2 = get_preset_theme("ARCANE")
        theme3 = get_preset_theme("Arcane")

        assert theme1 is not None
        assert theme2 is not None
        assert theme3 is not None
        assert theme1.name == theme2.name == theme3.name

    def test_get_preset_theme_not_found(self):
        """Test getting non-existent preset theme."""
        theme = get_preset_theme("nonexistent")
        assert theme is None

    def test_list_preset_themes(self):
        """Test listing all preset theme names."""
        themes = list_preset_themes()
        assert isinstance(themes, list)
        assert "default" in themes
        assert "arcane" in themes
        assert len(themes) >= 2


class TestThemeCompatibility:
    """Test Django Spellbook compatibility."""

    def test_theme_from_dict(self):
        """Test creating theme from dict (Django Spellbook format)."""
        theme_dict = {
            "name": "CustomTheme",
            "colors": {
                "primary": "#FF6B35",
                "accent": "#FFD700",
                "background": "#1a1a1a",
                "text": "#ffffff",
            },
            "generate_variants": True,
        }
        theme = Theme(**theme_dict)
        assert theme.name == "CustomTheme"
        assert theme.colors.primary == "#FF6B35"
        assert theme.generate_variants is True

    def test_theme_serialization(self):
        """Test theme can be serialized to dict."""
        colors = ThemeColors(primary="#FF6B35", accent="#FFD700")
        theme = Theme(name="Test", colors=colors)
        theme_dict = theme.model_dump()

        assert theme_dict["name"] == "Test"
        assert theme_dict["colors"]["primary"] == "#FF6B35"
        assert theme_dict["colors"]["accent"] == "#FFD700"
        assert theme_dict["generate_variants"] is True
