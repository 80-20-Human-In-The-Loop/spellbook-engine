# Baseline 02: Theme System Architecture

**Date**: 2025-09-29
**Status**: Implemented (Phase 1 & 2 Complete)
**Test Coverage**: 159 tests passing (60 new tests added)

## Overview

This baseline documents the implementation of a framework-agnostic theming system for Spellbook Engine that maintains 100% compatibility with Django Spellbook's theme format while remaining usable in any Python context.

## Architectural Decision

### Problem Statement

Built-in SpellBlocks need consistent, themeable styling that:
1. Works without a web framework (Flask, FastAPI, static sites)
2. Maintains compatibility with Django Spellbook's existing theme system
3. Requires zero build steps or preprocessing
4. Allows runtime theme customization
5. Uses semantic color naming (primary, accent, error, etc.)

### Solution: CSS Variables + Pydantic Models

We chose **CSS variables** over alternatives:

| Approach | Pros | Cons | Decision |
|----------|------|------|----------|
| **CSS Variables** | Browser-native, runtime changes, zero build, Django compatible | Requires modern browsers | ✅ **CHOSEN** |
| CSS-in-JS | Dynamic, component-scoped | Framework lock-in, build step | ❌ Rejected |
| SCSS/LESS | Powerful features | Build step required, not runtime | ❌ Rejected |
| Tailwind | Utility-first | Large CSS file, framework-specific | ❌ Rejected (future Phase 4) |
| Inline styles | No external CSS | Duplication, no reusability | ❌ Rejected |

**Why CSS Variables Won:**
- 🌐 **Browser-native** - No preprocessing or build tools
- ⚡ **Runtime dynamic** - Change themes without rebuilding
- 🔄 **Django compatible** - Same variable names as Django Spellbook
- 📦 **Framework agnostic** - Works anywhere HTML is rendered
- 🎨 **Modern CSS** - `color-mix()` for opacity variants

## Component Architecture

### Core Components

```
spellbook_engine/
├── theme.py              # NEW: Theme models and presets
│   ├── ThemeColors       # Pydantic model: 19 color fields
│   ├── Theme             # Complete theme configuration
│   └── PRESET_THEMES     # 5 preset themes (default, arcane, etc.)
│
├── styles.py             # UPDATED: Enhanced StyleCollector
│   ├── StyleSheet        # CSS metadata (unchanged)
│   ├── StyleRegistry     # Deduplication (unchanged)
│   └── StyleCollector    # NOW: Accepts optional theme
│
├── parser.py             # UPDATED: Theme parameter
│   └── SpellbookParser   # NEW: theme="arcane" or Theme object
│
└── __init__.py           # UPDATED: Export theme classes
```

### Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                   SpellbookParser(theme="arcane")            │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  1. Lookup preset theme by name                        │ │
│  │  2. Create StyleCollector with theme                   │ │
│  └────────────────────────────────────────────────────────┘ │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ↓
         ┌──────────────────────────────────────┐
         │   StyleCollector(theme=Theme)        │
         │  ┌────────────────────────────────┐  │
         │  │  During rendering:              │  │
         │  │  - Collect block styles        │  │
         │  │  - Store theme reference       │  │
         │  └────────────────────────────────┘  │
         └───────────────┬──────────────────────┘
                         │
                         ↓
         ┌──────────────────────────────────────┐
         │   StyleCollector.render()            │
         │  ┌────────────────────────────────┐  │
         │  │  1. Generate :root {} block    │  │
         │  │     with CSS variables         │  │
         │  │  2. Add block styles           │  │
         │  │  3. Return <style> tag         │  │
         │  └────────────────────────────────┘  │
         └──────────────────────────────────────┘
```

## Implementation Details

### ThemeColors Model

```python
class ThemeColors(BaseModel):
    # Core semantic colors (4)
    primary: str = "#3b82f6"
    secondary: str = "#6b7280"
    accent: str = "#f59e0b"
    neutral: str = "#2563eb"

    # Status colors (4)
    error: str = "#dc2626"
    warning: str = "#f59e0b"
    success: str = "#16a34a"
    info: str = "#2563eb"

    # Extended palette (7)
    emphasis: str = "#8b5cf6"
    subtle: str = "#f3f4f6"
    distinct: str = "#06b6d4"
    aether: str = "#c026d3"      # Magical theme
    artifact: str = "#a16207"    # Items/treasure
    sylvan: str = "#3f6212"      # Nature theme
    danger: str = "#a80000"      # Critical state

    # System colors (4)
    background: str = "#ffffff"
    surface: str = "#f9fafb"
    text: str = "#1f2937"
    text_secondary: str = "#6b7280"
```

**Total: 19 color fields** matching Django Spellbook exactly.

### Theme Model

```python
class Theme(BaseModel):
    name: str
    colors: ThemeColors = Field(default_factory=ThemeColors)
    generate_variants: bool = True  # Generate 25%, 50%, 75% opacity
    custom_colors: dict[str, str] | None = None

    def to_css_variables(self) -> dict[str, str]:
        """Generate all CSS variables including opacity variants."""

    def to_css_root_block(self) -> str:
        """Generate complete :root {} CSS block."""
```

### CSS Variable Generation

**Input (Theme):**
```python
Theme(
    name="Arcane",
    colors=ThemeColors(primary="#8b5cf6", accent="#fbbf24"),
    generate_variants=True
)
```

**Output (CSS):**
```css
:root {
  --accent-color: #fbbf24;
  --accent-color-25: color-mix(in srgb, #fbbf24 25%, transparent);
  --accent-color-50: color-mix(in srgb, #fbbf24 50%, transparent);
  --accent-color-75: color-mix(in srgb, #fbbf24 75%, transparent);
  --primary-color: #8b5cf6;
  --primary-color-25: color-mix(in srgb, #8b5cf6 25%, transparent);
  --primary-color-50: color-mix(in srgb, #8b5cf6 50%, transparent);
  --primary-color-75: color-mix(in srgb, #8b5cf6 75%, transparent);
  /* ... 19 colors × 4 variants each = 76 variables */
}
```

### Preset Themes

5 themes included matching common use cases:

| Theme | Primary | Use Case |
|-------|---------|----------|
| **default** | `#3b82f6` (blue) | General purpose, clean |
| **arcane** | `#8b5cf6` (purple) | Magical, mystical content |
| **forest** | `#059669` (green) | Nature, environmental |
| **crimson** | `#dc2626` (red) | Bold, dramatic |
| **ocean** | `#0891b2` (cyan) | Aquatic, tech |
| **sunset** | `#f97316` (orange) | Warm, energetic |

Each theme defines all 19 colors for full theming coverage.

## API Design

### Usage Examples

**Preset Theme by Name:**
```python
from spellbook_engine import SpellbookParser

parser = SpellbookParser(theme="arcane")
html = parser.render(markdown)
```

**Custom Theme Object:**
```python
from spellbook_engine import Theme, ThemeColors

colors = ThemeColors(
    primary="#FF6B35",
    accent="#FFD700",
    background="#1a1a1a",
    text="#ffffff"
)
theme = Theme(name="MyBrand", colors=colors)
parser = SpellbookParser(theme=theme)
html = parser.render(markdown)
```

**No Theme (Fallback Values):**
```python
parser = SpellbookParser()  # Theme is optional
html = parser.render(markdown)  # Uses fallback values in var()
```

**Invalid Theme Name:**
```python
parser = SpellbookParser(theme="nonexistent")
# Logs warning, falls back to no theme (parser.theme = None)
```

## Django Spellbook Compatibility

### Shared Format

Both Django Spellbook and Spellbook Engine accept identical theme definitions:

```python
# Works in BOTH packages
CUSTOM_THEME = {
    'name': 'MyTheme',
    'colors': {
        'primary': '#FF6B35',
        'accent': '#FFD700',
        # ... same 19 color fields
    },
    'generate_variants': True
}

# Django Spellbook (settings.py)
SPELLBOOK_THEME = CUSTOM_THEME

# Spellbook Engine (Python)
from spellbook_engine import Theme
theme = Theme(**CUSTOM_THEME)
parser = SpellbookParser(theme=theme)
```

### CSS Variable Naming

**Identical across both systems:**
- `--primary-color`, `--secondary-color`, `--accent-color`
- `--error-color`, `--warning-color`, `--success-color`, `--info-color`
- `--emphasis-color`, `--subtle-color`, `--distinct-color`
- `--aether-color`, `--artifact-color`, `--sylvan-color`, `--danger-color`
- `--background-color`, `--surface-color`, `--text-color`, `--text-secondary-color`

**Opacity variants:**
- `--primary-color-25`, `--primary-color-50`, `--primary-color-75`
- Same pattern for all 19 colors

This guarantees:
✅ Blocks work in both systems
✅ Themes are portable
✅ Same CSS works in Django and standalone engine

## Implementation Phases

### Phase 1: Theme Configuration ✅ **COMPLETE**
- ✅ Created `theme.py` with Pydantic models
- ✅ Added 5 preset themes
- ✅ Type-safe theme validation
- ✅ Django Spellbook format compatibility

### Phase 2: CSS Variable Injection ✅ **COMPLETE**
- ✅ Enhanced `StyleCollector` to accept theme
- ✅ CSS variable generation in `:root {}` block
- ✅ Opacity variant generation with `color-mix()`
- ✅ Updated `SpellbookParser` with theme parameter
- ✅ All 4 built-in blocks use CSS variables

### Phase 3: Theme Switching API 🚧 **DEFERRED**
- ⏳ Export theme to separate CSS file
- ⏳ Generate multiple theme CSS files for SSG
- ⏳ Theme change hooks for dynamic sites
- ⏳ Client-side theme switcher JavaScript

### Phase 4: Utility Class Generation 🚧 **DEFERRED**
- ⏳ Generate `sb-bg-{color}`, `sb-text-{color}` utilities
- ⏳ Generate hover states (`sb-hover:bg-{color}`)
- ⏳ Spacing utilities
- ⏳ Dark mode utilities

## Testing Strategy

### Test Coverage

**New Tests Added: 60**
**Total Tests: 159** (99 → 159)

**Breakdown:**
- `tests/unit/test_theme.py` - 22 tests
  - ThemeColors validation
  - Theme model creation
  - CSS variable generation
  - Preset theme validation
  - Django compatibility

- `tests/unit/test_styles.py` - 27 tests (NEW FILE)
  - StyleSheet hash deduplication
  - StyleRegistry sorting
  - StyleCollector without theme
  - StyleCollector with theme
  - CSS variable injection
  - Opacity variant generation

- `tests/integration/test_parser_integration.py` - 10 tests
  - Parser with preset theme name
  - Parser with custom Theme object
  - Parser with opacity variants
  - Parser without theme (fallback)
  - Invalid theme handling
  - All preset themes validation
  - Variable ordering (`:root` before blocks)
  - Multiple blocks with theme
  - Theme persistence across renders
  - Custom color variables

### Test Results

```
159 passed in 1.10s
```

**100% pass rate** ✅

## Performance Considerations

### Memory Impact
- Theme object: ~2KB per theme
- CSS variable generation: O(n) where n = 19 colors × 4 variants = 76 variables
- Cached in StyleCollector per render (not per block)

### Runtime Impact
- Theme lookup: O(1) dictionary lookup for presets
- CSS generation: Once per document render, not per block
- No measurable performance difference in tests

### CSS Size Impact
Without theme:
```html
<style>
/* alert */
.sb-alert { ... }
</style>
```
**Size: ~2KB**

With theme (variants enabled):
```html
<style>
:root { /* 76 variables */ }
/* alert */
.sb-alert { ... }
</style>
```
**Size: ~5KB** (+3KB for all variables)

The 3KB overhead is acceptable for complete theming capability.

## Design Decisions

### Why Pydantic for Theme Models?

**Pros:**
- Type validation at runtime
- IDE autocomplete for color fields
- Easy serialization to/from dict (Django compatibility)
- Validation errors are helpful
- Documentation via field descriptions

**Cons:**
- Adds dependency (but already used elsewhere)

**Decision:** ✅ Use Pydantic - benefits outweigh dependency cost

### Why `color-mix()` for Opacity?

**Alternatives:**
1. `rgba()` - Requires parsing hex to RGB
2. `opacity` property - Affects entire element
3. Pre-computed opacity colors - Inflexible

**Decision:** ✅ Use `color-mix()` - modern, flexible, matches Django Spellbook

### Why Optional Theme?

Making theme optional (vs. required) means:
- ✅ Zero breaking changes for existing users
- ✅ Simple start for new users
- ✅ Gradual adoption path
- ✅ Fallback values in `var()` work without theme

**Decision:** ✅ Theme is opt-in

### Why 5 Preset Themes?

**Rationale:**
- Covers common use cases (general, magical, nature, bold, tech)
- Small enough to maintain
- Large enough to demonstrate variety
- Matches Django Spellbook's approach

More presets can be added without breaking changes.

## Future Considerations

### Dark Mode (Phase 5?)

Not implemented yet, but architecture supports it:

```python
class Theme(BaseModel):
    name: str
    colors: ThemeColors
    dark_colors: ThemeColors | None = None  # Future

    def get_colors_for_mode(self, mode: str) -> ThemeColors:
        if mode == "dark" and self.dark_colors:
            return self.dark_colors
        return self.colors
```

Could generate:
```css
:root { /* light mode variables */ }
@media (prefers-color-scheme: dark) {
  :root { /* dark mode variables */ }
}
```

### Theme Interpolation (Phase 6?)

Blend between themes for animations:

```python
def interpolate_themes(theme1: Theme, theme2: Theme, t: float) -> Theme:
    """Interpolate between two themes (t from 0 to 1)."""
    # Blend hex colors
```

### A11y Contrast Checking (Phase 6?)

Validate color combinations meet WCAG standards:

```python
def check_contrast(theme: Theme) -> list[str]:
    """Return list of contrast warnings."""
    warnings = []
    if contrast_ratio(theme.colors.text, theme.colors.background) < 4.5:
        warnings.append("Text/background contrast too low")
    return warnings
```

## Migration Path

### For Existing Spellbook Engine Users

**No changes required:**
```python
# Existing code continues to work
parser = SpellbookParser()
html = parser.render(markdown)  # Still works!
```

**Opt-in to theming:**
```python
# Add theme parameter when ready
parser = SpellbookParser(theme="arcane")
```

### For Django Spellbook Users

**Engine-rendered content gets theme automatically:**
```python
# In Django view
from spellbook_engine import SpellbookParser
from django_spellbook.theme import get_current_theme

def my_view(request):
    theme = get_current_theme(request)  # From session
    parser = SpellbookParser(theme=theme)  # Pass to engine
    html = parser.render(markdown)
    return render(request, "template.html", {"content": html})
```

## Lessons Learned

### What Went Well
1. **Pydantic validation** caught invalid colors early
2. **CSS variables** were simpler than expected
3. **Django compatibility** achieved with zero compromises
4. **Test-first approach** prevented regressions
5. **Optional design** meant zero breaking changes

### What Could Be Improved
1. **Color validation** is basic (just non-empty string) - could validate hex format
2. **Preset themes** could have more variety (only 5 currently)
3. **Documentation** for theme creation could be more detailed
4. **Type hints** for `theme` parameter could be more specific (Union[str, Theme, None])

### If We Did It Again
- Consider **color validation** with regex for hex/rgb/hsl
- Add **theme builder CLI** earlier for easier customization
- Generate **theme preview HTML** during tests
- Add **contrast ratio calculator** from the start

## Related Documents

- `__architecture/styles/01_style_system_overview.md` - Style collection system
- `__architecture/styles/02_custom_styles_guide.md` - Using CSS variables in custom blocks
- `__architecture/styles/03_theming_future.md` - Original roadmap (Phases 3-4)

## Summary

The theme system successfully achieves:
- ✅ **Framework agnostic** - Works in any Python context
- ✅ **Django compatible** - Same CSS variables and theme format
- ✅ **Type safe** - Pydantic validation
- ✅ **Zero build** - CSS generated at runtime
- ✅ **Optional** - No breaking changes
- ✅ **Well tested** - 60 new tests, 100% passing
- ✅ **Extensible** - Ready for Phases 3-4

**Phase 1 & 2 Status**: ✅ **COMPLETE**