# Custom Styles Guide

Guide for adding styles to your custom SpellBlocks.

## Using Spellbook Theme Colors

Spellbook Engine supports the same CSS variable system as Django Spellbook's theme system. All built-in blocks use these variables for automatic theming.

### Available Theme Variables

```css
/* Core Semantic Colors */
--primary-color: #3b82f6;
--secondary-color: #6b7280;
--accent-color: #f59e0b;
--neutral-color: #2563eb;

/* Status Colors */
--error-color: #dc2626;
--warning-color: #f59e0b;
--success-color: #16a34a;
--info-color: #2563eb;

/* Extended Palette (from Django Spellbook) */
--emphasis-color: #8b5cf6;
--subtle-color: #f3f4f6;
--distinct-color: #06b6d4;
--aether-color: #c026d3;
--artifact-color: #a16207;
--sylvan-color: #3f6212;
--danger-color: #a80000;

/* System Colors */
--background-color: #ffffff;
--surface-color: #f9fafb;
--text-color: #1f2937;
--text-secondary-color: #6b7280;
```

## Method 1: Python `get_styles()` Method (Recommended)

Define styles directly in your block class using theme variables.

### Basic Example with Theme Colors

```python
from spellbook_engine import BaseSpellBlock
from typing import Any

class FeatureBoxBlock(BaseSpellBlock):
    """Feature box using theme colors."""

    def get_context(self) -> dict[str, Any]:
        return {
            "content": self.process_content(),
            "color": self.kwargs.get("color", "primary"),
            "icon": self.kwargs.get("icon", "✨"),
        }

    def get_styles(self) -> str:
        """Return CSS styles using theme variables."""
        return """
.sb-feature-box {
    padding: 24px;
    margin: 16px 0;
    border-radius: 12px;
    background-color: var(--surface-color, #f9fafb);
    border: 2px solid var(--subtle-color, #e5e7eb);
    transition: all 0.3s ease;
}

.sb-feature-box:hover {
    border-color: var(--primary-color, #3b82f6);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.sb-feature-box-primary {
    border-color: var(--primary-color, #3b82f6);
}

.sb-feature-box-accent {
    border-color: var(--accent-color, #f59e0b);
}

.sb-feature-box-aether {
    border-color: var(--aether-color, #c026d3);
}

.sb-feature-box-icon {
    font-size: 2em;
    color: var(--text-color, #1f2937);
}
"""

    def get_style_priority(self) -> int:
        return 10
```

### With Opacity Variants (color-mix)

Use `color-mix()` for opacity variants, matching Django Spellbook's utility system:

```python
def get_styles(self) -> str:
    return """
.sb-callout {
    padding: 20px;
    margin: 16px 0;
    border-radius: 8px;
    /* 25% opacity background */
    background-color: color-mix(
        in srgb,
        var(--info-color, #2563eb) 25%,
        transparent
    );
    border-left: 4px solid var(--info-color, #2563eb);
}

.sb-callout-warning {
    background-color: color-mix(
        in srgb,
        var(--warning-color, #f59e0b) 25%,
        transparent
    );
    border-left-color: var(--warning-color, #f59e0b);
}

.sb-callout-success {
    background-color: color-mix(
        in srgb,
        var(--success-color, #16a34a) 25%,
        transparent
    );
    border-left-color: var(--success-color, #16a34a);
}
"""
```

## Method 2: External CSS File

For larger stylesheets, keep CSS in a separate file.

### File Structure
```
my_blocks/
├── logic/
│   └── hero.py
├── templates/
│   └── hero.html
└── styles/
    └── hero.css
```

### In your block class:

```python
from pathlib import Path

class HeroBlock(BaseSpellBlock):
    def get_styles(self) -> str:
        """Load styles from external CSS file."""
        css_path = Path(__file__).parent.parent / "styles" / "hero.css"
        return css_path.read_text()
```

### hero.css (using theme variables)
```css
.sb-hero {
    display: flex;
    align-items: center;
    gap: 24px;
    padding: 48px;
    background: var(--background-color, #ffffff);
    color: var(--text-color, #1f2937);
}

.sb-hero-accent {
    background: linear-gradient(
        135deg,
        var(--primary-color, #3b82f6),
        var(--accent-color, #f59e0b)
    );
    color: white;
}

.sb-hero-image {
    flex: 1;
    border-radius: 12px;
    border: 2px solid var(--subtle-color, #f3f4f6);
}

.sb-hero-content {
    flex: 2;
}
```

## Utility-First Approach

You can also use Spellbook's utility classes in your templates (if you're using Django Spellbook):

```html
<div class="sb-bg-primary sb-text-white sb-p-6 sb-rounded-lg">
    <h3 class="sb-text-xl sb-font-bold">{{ title }}</h3>
    <p class="sb-text-secondary-75">{{ content }}</p>
</div>
```

Available utility patterns (from Django Spellbook):
- `sb-bg-{color}` - Background colors
- `sb-text-{color}` - Text colors
- `sb-border-{color}` - Border colors
- `sb-bg-{color}-{25|50|75}` - Opacity variants
- `sb-hover:bg-{color}` - Hover states

## Style Naming Conventions

### Namespace ALL classes with `sb-`

```css
/* ✅ GOOD - Namespaced */
.sb-myblock { }
.sb-myblock-header { }
.sb-myblock-title { }

/* ❌ BAD - Will conflict */
.myblock { }
.header { }
.title { }
```

### Block-specific prefixes

```css
/* For a "callout" block */
.sb-callout { }
.sb-callout-info { }
.sb-callout-warning { }

/* For a "timeline" block */
.sb-timeline { }
.sb-timeline-item { }
.sb-timeline-marker { }
```

## Theme Color Categories

### When to use each color:

**Primary** - Main brand color, primary actions
```css
.sb-button-primary {
    background-color: var(--primary-color, #3b82f6);
}
```

**Accent** - Call-to-action, highlights, emphasis
```css
.sb-badge-featured {
    background-color: var(--accent-color, #f59e0b);
}
```

**Neutral** - Borders, dividers, subtle backgrounds
```css
.sb-divider {
    border-color: var(--neutral-color, #e5e7eb);
}
```

**Emphasis** - Special content, magical elements
```css
.sb-highlight {
    background-color: var(--emphasis-color, #8b5cf6);
}
```

**Aether/Artifact/Sylvan** - Themed categories (magic, special items, nature)
```css
.sb-spell-card {
    border-color: var(--aether-color, #c026d3);
}

.sb-item-card {
    border-color: var(--artifact-color, #a16207);
}

.sb-nature-badge {
    background-color: var(--sylvan-color, #3f6212);
}
```

## Best Practices

### 1. Always Use CSS Variables with Fallbacks

```css
/* ✅ GOOD - Themeable with fallback */
.sb-panel {
    background-color: var(--surface-color, #f9fafb);
    color: var(--text-color, #1f2937);
}

/* ❌ BAD - Hard-coded, not themeable */
.sb-panel {
    background-color: #f9fafb;
    color: #1f2937;
}
```

### 2. Use Semantic Variables

```css
/* ✅ GOOD - Semantic meaning */
.sb-error-message {
    color: var(--error-color, #dc2626);
}

/* ❌ BAD - Hard-coded color */
.sb-error-message {
    color: #dc2626;
}
```

### 3. Leverage Opacity Variants

```css
/* Subtle background with 25% opacity */
.sb-info-box {
    background-color: color-mix(
        in srgb,
        var(--info-color, #2563eb) 25%,
        transparent
    );
}

/* Semi-transparent overlay with 50% opacity */
.sb-overlay {
    background-color: color-mix(
        in srgb,
        var(--primary-color, #3b82f6) 50%,
        transparent
    );
}
```

### 4. Smooth Transitions

```css
.sb-card {
    transition: box-shadow 0.2s ease, transform 0.2s ease, border-color 0.2s ease;
}

.sb-card:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    transform: translateY(-2px);
    border-color: var(--primary-color, #3b82f6);
}
```

### 5. Accessibility

```css
/* Focus states */
.sb-button:focus {
    outline: 2px solid var(--primary-color, #3b82f6);
    outline-offset: 2px;
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
    .sb-card {
        transition: none;
    }
}
```

## Complete Working Example

```python
from spellbook_engine import BaseSpellBlock
from typing import Any

class StatusBannerBlock(BaseSpellBlock):
    """Status banner with theme colors."""

    def get_context(self) -> dict[str, Any]:
        return {
            "content": self.process_content(),
            "type": self.kwargs.get("type", "info"),  # info, warning, success, error
            "dismissible": self.kwargs.get("dismissible", False),
        }

    def get_styles(self) -> str:
        return """
.sb-status-banner {
    padding: 16px 24px;
    margin: 16px 0;
    border-radius: 8px;
    border-left: 4px solid;
    display: flex;
    align-items: center;
    gap: 12px;
}

.sb-status-banner-info {
    background-color: color-mix(in srgb, var(--info-color, #2563eb) 15%, transparent);
    border-left-color: var(--info-color, #2563eb);
    color: var(--text-color, #1f2937);
}

.sb-status-banner-warning {
    background-color: color-mix(in srgb, var(--warning-color, #f59e0b) 15%, transparent);
    border-left-color: var(--warning-color, #f59e0b);
    color: var(--text-color, #1f2937);
}

.sb-status-banner-success {
    background-color: color-mix(in srgb, var(--success-color, #16a34a) 15%, transparent);
    border-left-color: var(--success-color, #16a34a);
    color: var(--text-color, #1f2937);
}

.sb-status-banner-error {
    background-color: color-mix(in srgb, var(--error-color, #dc2626) 15%, transparent);
    border-left-color: var(--error-color, #dc2626);
    color: var(--text-color, #1f2937);
}

.sb-status-banner-close {
    margin-left: auto;
    background: none;
    border: none;
    cursor: pointer;
    color: var(--text-secondary-color, #6b7280);
    font-size: 1.2em;
}

.sb-status-banner-close:hover {
    color: var(--text-color, #1f2937);
}
"""

    def get_style_priority(self) -> int:
        return 10
```

### Template:

```html
<div class="sb-status-banner sb-status-banner-{{ type }}">
    <span class="sb-status-banner-content">{{ content }}</span>
    {% if dismissible %}
    <button class="sb-status-banner-close" onclick="this.parentElement.remove()">×</button>
    {% endif %}
</div>
```

### Usage:

```markdown
{~ status_banner type="success" ~}
Your changes have been saved successfully!
{~~}

{~ status_banner type="warning" dismissible="true" ~}
This action cannot be undone. Please review carefully.
{~~}
```

## Integration with Django Spellbook

If you're using both engines together, you can share the theme system:

1. **In Django** - Set theme in `settings.py`:
```python
from django_spellbook.theme import THEMES_WITH_MODES

SPELLBOOK_THEME = THEMES_WITH_MODES['arcane']['modes']['light']
```

2. **Engine blocks automatically use theme colors** - All CSS variables will be consistent

3. **Mix utility classes with custom blocks**:
```html
<div class="sb-bg-surface sb-p-6 sb-rounded-lg">
    {~ feature_box icon="🚀" color="primary" ~}
    This uses both utilities AND custom block styling!
    {~~}
</div>
```

## Next Steps

- See `03_theming_future.md` for upcoming theming features
- Check Django Spellbook docs for full theme system: https://docs.django-spellbook.com/themes/
- Use the theme builder to create custom palettes visually