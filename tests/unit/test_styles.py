"""Tests for the style management system."""

from spellbook_engine.styles import StyleCollector, StyleRegistry, StyleSheet
from spellbook_engine.theme import Theme, ThemeColors


class TestStyleSheet:
    """Test StyleSheet model."""

    def test_stylesheet_creation(self):
        """Test basic stylesheet creation."""
        sheet = StyleSheet(
            block_name="alert",
            css=".sb-alert { color: red; }",
            priority=0,
        )
        assert sheet.block_name == "alert"
        assert sheet.css == ".sb-alert { color: red; }"
        assert sheet.priority == 0
        assert sheet.hash  # Hash should be generated

    def test_stylesheet_hash_generation(self):
        """Test that hash is automatically generated."""
        css = ".sb-card { padding: 10px; }"
        sheet1 = StyleSheet(block_name="card", css=css)
        sheet2 = StyleSheet(block_name="card", css=css)

        # Same CSS should produce same hash
        assert sheet1.hash == sheet2.hash

    def test_stylesheet_different_hash(self):
        """Test that different CSS produces different hash."""
        sheet1 = StyleSheet(block_name="alert", css=".sb-alert { color: red; }")
        sheet2 = StyleSheet(block_name="alert", css=".sb-alert { color: blue; }")

        assert sheet1.hash != sheet2.hash

    def test_stylesheet_default_priority(self):
        """Test default priority is 10 (user blocks)."""
        sheet = StyleSheet(block_name="test", css=".test {}")
        assert sheet.priority == 10


class TestStyleRegistry:
    """Test StyleRegistry."""

    def test_registry_initialization(self):
        """Test registry starts empty."""
        registry = StyleRegistry()
        assert len(registry.get_all_styles()) == 0

    def test_register_stylesheet(self):
        """Test registering a stylesheet."""
        registry = StyleRegistry()
        sheet = StyleSheet(block_name="alert", css=".sb-alert {}", priority=0)

        result = registry.register(sheet)
        assert result is True
        assert len(registry.get_all_styles()) == 1

    def test_register_duplicate_stylesheet(self):
        """Test that duplicate stylesheets are rejected."""
        registry = StyleRegistry()
        css = ".sb-alert { color: red; }"
        sheet1 = StyleSheet(block_name="alert", css=css)
        sheet2 = StyleSheet(block_name="alert", css=css)

        assert registry.register(sheet1) is True
        assert registry.register(sheet2) is False  # Duplicate
        assert len(registry.get_all_styles()) == 1

    def test_register_different_stylesheets(self):
        """Test registering multiple different stylesheets."""
        registry = StyleRegistry()
        sheet1 = StyleSheet(block_name="alert", css=".sb-alert {}")
        sheet2 = StyleSheet(block_name="card", css=".sb-card {}")

        assert registry.register(sheet1) is True
        assert registry.register(sheet2) is True
        assert len(registry.get_all_styles()) == 2

    def test_get_all_styles_sorted_by_priority(self):
        """Test that styles are returned sorted by priority."""
        registry = StyleRegistry()
        sheet1 = StyleSheet(block_name="user", css=".user {}", priority=10)
        sheet2 = StyleSheet(block_name="builtin", css=".builtin {}", priority=0)
        sheet3 = StyleSheet(block_name="inline", css=".inline {}", priority=20)

        registry.register(sheet1)
        registry.register(sheet3)
        registry.register(sheet2)

        styles = registry.get_all_styles()
        assert len(styles) == 3
        assert styles[0].priority == 0  # builtin
        assert styles[1].priority == 10  # user
        assert styles[2].priority == 20  # inline

    def test_clear_registry(self):
        """Test clearing the registry."""
        registry = StyleRegistry()
        sheet = StyleSheet(block_name="alert", css=".sb-alert {}")
        registry.register(sheet)

        assert len(registry.get_all_styles()) == 1
        registry.clear()
        assert len(registry.get_all_styles()) == 0


class TestStyleCollector:
    """Test StyleCollector without theme."""

    def test_collector_initialization(self):
        """Test collector initialization."""
        collector = StyleCollector()
        assert collector.registry is not None
        assert collector.theme is None

    def test_add_style(self):
        """Test adding a style."""
        collector = StyleCollector()
        result = collector.add_style(
            block_name="alert",
            css=".sb-alert { color: red; }",
            priority=0,
        )
        assert result is True

    def test_add_duplicate_style(self):
        """Test that duplicate styles are not added."""
        collector = StyleCollector()
        css = ".sb-alert { color: red; }"

        result1 = collector.add_style(block_name="alert", css=css)
        result2 = collector.add_style(block_name="alert", css=css)

        assert result1 is True
        assert result2 is False

    def test_render_empty_collector(self):
        """Test rendering with no styles."""
        collector = StyleCollector()
        output = collector.render()
        assert output == ""

    def test_render_single_style(self):
        """Test rendering a single style."""
        collector = StyleCollector()
        collector.add_style(
            block_name="alert",
            css=".sb-alert { color: red; }",
            priority=0,
        )

        output = collector.render()
        assert output.startswith("<style>")
        assert output.endswith("</style>")
        assert "/* alert */" in output
        assert ".sb-alert { color: red; }" in output

    def test_render_multiple_styles(self):
        """Test rendering multiple styles."""
        collector = StyleCollector()
        collector.add_style(block_name="alert", css=".sb-alert {}", priority=0)
        collector.add_style(block_name="card", css=".sb-card {}", priority=0)

        output = collector.render()
        assert "/* alert */" in output
        assert "/* card */" in output
        assert ".sb-alert {}" in output
        assert ".sb-card {}" in output

    def test_render_respects_priority(self):
        """Test that rendering respects priority order."""
        collector = StyleCollector()
        collector.add_style(block_name="user", css=".user {}", priority=10)
        collector.add_style(block_name="builtin", css=".builtin {}", priority=0)

        output = collector.render()
        # Builtin (priority 0) should come before user (priority 10)
        builtin_pos = output.find(".builtin")
        user_pos = output.find(".user")
        assert builtin_pos < user_pos

    def test_clear_collector(self):
        """Test clearing the collector."""
        collector = StyleCollector()
        collector.add_style(block_name="alert", css=".sb-alert {}")

        output = collector.render()
        assert output != ""

        collector.clear()
        output = collector.render()
        assert output == ""


class TestStyleCollectorWithTheme:
    """Test StyleCollector with theme support."""

    def test_collector_with_theme(self):
        """Test collector initialization with theme."""
        colors = ThemeColors(primary="#FF6B35")
        theme = Theme(name="Test", colors=colors, generate_variants=False)
        collector = StyleCollector(theme=theme)

        assert collector.theme is not None
        assert collector.theme.name == "Test"

    def test_render_with_theme_no_styles(self):
        """Test rendering only theme variables with no block styles."""
        colors = ThemeColors(primary="#FF6B35")
        theme = Theme(name="Test", colors=colors, generate_variants=False)
        collector = StyleCollector(theme=theme)

        output = collector.render()
        assert output.startswith("<style>")
        assert ":root {" in output
        assert "--primary-color: #FF6B35;" in output

    def test_render_with_theme_and_styles(self):
        """Test rendering theme variables with block styles."""
        colors = ThemeColors(primary="#FF6B35")
        theme = Theme(name="Test", colors=colors, generate_variants=False)
        collector = StyleCollector(theme=theme)

        collector.add_style(block_name="alert", css=".sb-alert { color: red; }")

        output = collector.render()
        assert ":root {" in output
        assert "--primary-color: #FF6B35;" in output
        assert "/* alert */" in output
        assert ".sb-alert { color: red; }" in output

        # Theme variables should come before block styles
        root_pos = output.find(":root")
        alert_pos = output.find("/* alert */")
        assert root_pos < alert_pos

    def test_render_with_theme_variants(self):
        """Test rendering with opacity variants."""
        colors = ThemeColors(primary="#FF6B35")
        theme = Theme(name="Test", colors=colors, generate_variants=True)
        collector = StyleCollector(theme=theme)

        output = collector.render()
        assert "--primary-color: #FF6B35;" in output
        assert "--primary-color-25:" in output
        assert "color-mix(in srgb, #FF6B35 25%, transparent)" in output
        assert "--primary-color-50:" in output
        assert "--primary-color-75:" in output

    def test_render_theme_with_custom_colors(self):
        """Test rendering theme with custom color variables."""
        theme = Theme(
            name="Test",
            custom_colors={
                "brand-primary": "#123456",
                "brand-accent": "#abcdef",
            },
        )
        collector = StyleCollector(theme=theme)

        output = collector.render()
        assert "--brand-primary: #123456;" in output
        assert "--brand-accent: #abcdef;" in output

    def test_theme_with_all_preset_themes(self):
        """Test that all preset themes work with collector."""
        from spellbook_engine import PRESET_THEMES

        for _theme_name, theme in PRESET_THEMES.items():
            collector = StyleCollector(theme=theme)
            output = collector.render()

            # Should have :root block
            assert ":root {" in output

            # Should have all standard color variables
            assert "--primary-color:" in output
            assert "--secondary-color:" in output
            assert "--accent-color:" in output
            assert "--error-color:" in output
            assert "--background-color:" in output


class TestStyleCollectorEdgeCases:
    """Test edge cases for StyleCollector."""

    def test_collector_reuse_after_clear(self):
        """Test collector can be reused after clearing."""
        collector = StyleCollector()
        collector.add_style(block_name="alert", css=".sb-alert {}")

        output1 = collector.render()
        assert ".sb-alert {}" in output1

        collector.clear()
        collector.add_style(block_name="card", css=".sb-card {}")

        output2 = collector.render()
        assert ".sb-card {}" in output2
        assert ".sb-alert {}" not in output2

    def test_collector_with_empty_css(self):
        """Test adding style with empty CSS."""
        collector = StyleCollector()
        collector.add_style(block_name="empty", css="")

        output = collector.render()
        assert "/* empty */" in output

    def test_multiple_collectors_independent(self):
        """Test that multiple collectors are independent."""
        collector1 = StyleCollector()
        collector2 = StyleCollector()

        collector1.add_style(block_name="alert", css=".sb-alert {}")
        collector2.add_style(block_name="card", css=".sb-card {}")

        output1 = collector1.render()
        output2 = collector2.render()

        assert ".sb-alert {}" in output1
        assert ".sb-alert {}" not in output2
        assert ".sb-card {}" in output2
        assert ".sb-card {}" not in output1
