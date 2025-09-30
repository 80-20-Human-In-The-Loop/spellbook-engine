# Theming System - Future Roadmap

Integration plan for Django Spellbook's theme system into Spellbook Engine.

## Current State

**Spellbook Engine** (this repo):
- ✅ Style collection and deduplication system
- ✅ CSS variables in built-in blocks
- ✅ `get_styles()` API for custom blocks
- ❌ No theme configuration system yet

**Django Spellbook** (separate package):
- ✅ Full Python-based theme system
- ✅ 9 preset themes with light/dark modes
- ✅ Session-based theme switching
- ✅ Automatic CSS variable generation
- ✅ Opacity variants with `color-mix()`
- ✅ Visual theme builder UI

## Integration Goal

Make Spellbook Engine's theming system **framework-agnostic** while staying **100% compatible** with Django Spellbook.

## Phase 1: Theme Configuration (Planned)

### Add `spellbook_engine/theme.py`

```python
from pydantic import BaseModel
from typing import Dict, Optional

class ThemeColors(BaseModel):
    """Color palette for a theme."""
    # Core colors
    primary: str = "#3b82f6"
    secondary: str = "#6b7280"
    accent: str = "#f59e0b"
    neutral: str = "#2563eb"

    # Status colors
    error: str = "#dc2626"
    warning: str = "#f59e0b"
    success: str = "#16a34a"
    info: str = "#2563eb"

    # Extended palette
    emphasis: str = "#8b5cf6"
    subtle: str = "#f3f4f6"
    distinct: str = "#06b6d4"
    aether: str = "#c026d3"
    artifact: str = "#a16207"
    sylvan: str = "#3f6212"
    danger: str = "#a80000"

    # System colors
    background: str = "#ffffff"
    surface: str = "#f9fafb"
    text: str = "#1f2937"
    text_secondary: str = "#6b7280"

class Theme(BaseModel):
    """Complete theme configuration."""
    name: str
    colors: ThemeColors
    generate_variants: bool = True
    custom_colors: Optional[Dict[str, str]] = None

# Preset themes from Django Spellbook
PRESET_THEMES = {
    "default": Theme(name="Default", colors=ThemeColors()),
    "arcane": Theme(name="Arcane", colors=ThemeColors(
        primary="#8b5cf6",
        accent="#fbbf24",
        aether="#c026d3",
        # ... rest of arcane colors
    )),
    # ... other presets
}
```

### Usage:

```python
from spellbook_engine import SpellbookParser, Theme

# Use preset theme
parser = SpellbookParser(theme="arcane")

# Or custom theme
custom_theme = Theme(
    name="MyBrand",
    colors=ThemeColors(
        primary="#FF6B35",
        accent="#FFD700",
    )
)
parser = SpellbookParser(theme=custom_theme)
```

## Phase 2: CSS Variable Injection

### StyleCollector Enhancement

```python
class StyleCollector:
    def __init__(self, theme: Optional[Theme] = None):
        self.registry = StyleRegistry()
        self.theme = theme

    def render(self) -> str:
        """Render styles with theme variables prepended."""
        styles = self.registry.get_all_styles()
        if not styles:
            return ""

        css_parts = []

        # Add theme variables at top if theme is set
        if self.theme:
            css_parts.append(":root {")
            for color_name, color_value in self.theme.colors.dict().items():
                css_name = color_name.replace("_", "-")
                css_parts.append(f"  --{css_name}-color: {color_value};")

                # Generate opacity variants
                if self.theme.generate_variants:
                    for opacity in [25, 50, 75]:
                        css_parts.append(
                            f"  --{css_name}-color-{opacity}: "
                            f"color-mix(in srgb, {color_value} {opacity}%, transparent);"
                        )
            css_parts.append("}")
            css_parts.append("")

        # Add block styles
        for stylesheet in styles:
            css_parts.append(f"/* {stylesheet.block_name} */")
            css_parts.append(stylesheet.css)
            css_parts.append("")

        combined_css = "\n".join(css_parts)
        return f"<style>\n{combined_css}\n</style>"
```

### Output Example:

```html
<style>
:root {
  --primary-color: #8b5cf6;
  --primary-color-25: color-mix(in srgb, #8b5cf6 25%, transparent);
  --primary-color-50: color-mix(in srgb, #8b5cf6 50%, transparent);
  --primary-color-75: color-mix(in srgb, #8b5cf6 75%, transparent);
  --accent-color: #fbbf24;
  /* ... */
}

/* alert */
.sb-alert {
    background-color: var(--surface-color, #f9fafb);
    /* ... */
}

/* card */
.sb-card {
    border-color: var(--subtle-color, #f3f4f6);
    /* ... */
}
</style>
```

## Phase 3: Theme Switching API

### For static site generators:

```python
from spellbook_engine import SpellbookParser, PRESET_THEMES

# Generate CSS for each theme
themes_css = {}
for theme_name, theme in PRESET_THEMES.items():
    parser = SpellbookParser(theme=theme)
    html = parser.render(markdown_content)
    themes_css[theme_name] = parser.style_collector.render()

# Write to separate CSS files
for theme_name, css in themes_css.items():
    Path(f"themes/{theme_name}.css").write_text(css)
```

### For dynamic sites (Django integration):

```python
# In Django view
from spellbook_engine import SpellbookParser
from django_spellbook.theme import get_current_theme

def my_view(request):
    theme = get_current_theme(request)  # From session
    parser = SpellbookParser(theme=theme)
    html = parser.render(markdown_content)
    return render(request, "template.html", {"content": html})
```

## Phase 4: Utility Class Generation (Optional)

Generate utility classes like Django Spellbook's system:

```python
class ThemeUtilityGenerator:
    """Generate utility classes from theme."""

    def generate(self, theme: Theme) -> str:
        """Generate CSS utility classes."""
        css = []

        for color_name, color_value in theme.colors.dict().items():
            css_name = color_name.replace("_", "-")

            # Background utilities
            css.append(f".sb-bg-{css_name} {{")
            css.append(f"  background-color: var(--{css_name}-color, {color_value});")
            css.append("}")

            # Text utilities
            css.append(f".sb-text-{css_name} {{")
            css.append(f"  color: var(--{css_name}-color, {color_value});")
            css.append("}")

            # Border utilities
            css.append(f".sb-border-{css_name} {{")
            css.append(f"  border-color: var(--{css_name}-color, {color_value});")
            css.append("}")

            # Opacity variants
            if theme.generate_variants:
                for opacity in [25, 50, 75]:
                    css.append(f".sb-bg-{css_name}-{opacity} {{")
                    css.append(f"  background-color: var(--{css_name}-color-{opacity});")
                    css.append("}")

        return "\n".join(css)
```

## Django Spellbook Compatibility

### Shared Theme Format

Both packages will use identical theme definitions:

```python
# Works in BOTH Django Spellbook and Spellbook Engine
ARCANE_THEME = {
    'colors': {
        'primary': '#8b5cf6',
        'accent': '#fbbf24',
        # ... rest of colors
    },
    'generate_variants': True,
}

# Django Spellbook (settings.py)
SPELLBOOK_THEME = ARCANE_THEME

# Spellbook Engine (Python)
from spellbook_engine import Theme
theme = Theme(**ARCANE_THEME)
parser = SpellbookParser(theme=theme)
```

### CSS Variable Compatibility

Both systems generate identical CSS variables:
- Same naming: `--primary-color`, `--accent-color`, etc.
- Same opacity format: `color-mix(in srgb, ...)`
- Same fallback values

This means:
- Blocks work in both systems
- Themes are portable
- Utilities are compatible

## Implementation Timeline

**v0.2.0** (Q2 2025):
- [ ] Add `theme.py` with `Theme` and `ThemeColors` models
- [ ] Add preset themes from Django Spellbook
- [ ] Update `StyleCollector` to inject CSS variables
- [ ] Add theme parameter to `SpellbookParser`

**v0.3.0** (Q3 2025):
- [ ] Add utility class generation
- [ ] Theme validation and color contrast checking
- [ ] Export theme to separate CSS file
- [ ] Theme documentation generator

**v0.4.0** (Q4 2025):
- [ ] Dark mode support (automatic inversion)
- [ ] Theme interpolation (blend between themes)
- [ ] A11y contrast warnings
- [ ] Visual theme builder CLI

## Benefits

1. **Framework Agnostic** - Use themes in Flask, FastAPI, static sites
2. **100% Compatible** - Works seamlessly with Django Spellbook
3. **Portable** - Same theme works everywhere
4. **Type Safe** - Pydantic validation for themes
5. **No Build Step** - CSS generated at runtime
6. **SSG Friendly** - Pre-generate theme CSS files

## Design Decisions

### Why Pydantic?

- Type validation for theme colors
- Easy serialization to/from dict
- IDE autocomplete support
- Compatible with Django Spellbook's structure

### Why CSS Variables?

- Browser-native theming
- No preprocessing required
- Can be overridden per-page
- Works with Django Spellbook's system

### Why color-mix()?

- Modern CSS feature for opacity
- Better than rgba() for theming
- Matches Django Spellbook's implementation
- Graceful fallback support

## Migration Path

For Django Spellbook users:

1. **No changes required** - Django package handles everything
2. **Gradual adoption** - Add engine-rendered content piece by piece
3. **Theme sync** - Engine reads Django's `SPELLBOOK_THEME` setting
4. **Shared blocks** - Same blocks work in both systems

For new Spellbook Engine users:

1. **Start simple** - Use preset themes
2. **Customize** - Override specific colors
3. **Scale up** - Generate utilities when needed
4. **Bridge to Django** - Easy migration if you need it

## Open Questions

1. **Should utilities be opt-in or automatic?**
   - Large CSS file vs. convenience
   - Leaning towards opt-in

2. **Should we support CSS frameworks (Tailwind, Bootstrap)?**
   - Could detect and integrate
   - But prefer our own system

3. **How to handle user theme uploads?**
   - Security concerns
   - Validation requirements

## Next Steps

1. Create `spellbook_engine/theme.py` with models
2. Port preset themes from Django Spellbook
3. Update `StyleCollector` to inject variables
4. Write integration tests
5. Document theme API

---

**Current Status**: Planning phase
**Target Release**: v0.2.0
**Compatibility**: Django Spellbook v0.1.16+