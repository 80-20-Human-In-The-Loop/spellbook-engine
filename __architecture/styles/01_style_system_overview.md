# Style Management System Overview

## Architecture

Spellbook Engine implements a smart style management system that automatically deduplicates and collects CSS styles during rendering.

### Core Components

```
┌─────────────────────────────────────────────────────────────┐
│                     SpellbookParser                          │
│  ┌────────────────────────────────────────────────────────┐ │
│  │           StyleCollector (one per render)               │ │
│  │  ┌──────────────────────────────────────────────────┐  │ │
│  │  │     StyleRegistry (hash-based deduplication)      │  │ │
│  │  │                                                    │  │ │
│  │  │  - Tracks loaded style hashes                     │  │ │
│  │  │  - Stores StyleSheet objects                      │  │ │
│  │  │  - Prevents duplicate styles                      │  │ │
│  │  └──────────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              ↓
                    render() is called
                              ↓
      ┌───────────────────────────────────────┐
      │  Process each SpellBlock encountered   │
      │                                         │
      │  1. Call block.get_styles()            │
      │  2. Add to StyleCollector              │
      │  3. Render block HTML (no styles)      │
      └───────────────────────────────────────┘
                              ↓
                  All blocks processed
                              ↓
      ┌───────────────────────────────────────┐
      │   StyleCollector.render()              │
      │                                         │
      │   - Sort styles by priority            │
      │   - Group with block name comments     │
      │   - Output single <style> tag          │
      └───────────────────────────────────────┘
                              ↓
              Append to end of HTML
```

### Key Classes

#### `StyleSheet` (Pydantic Model)
```python
class StyleSheet(BaseModel):
    block_name: str       # Name of the block (e.g., "alert", "card")
    css: str             # The actual CSS content
    priority: int        # 0=builtin, 10=user, 20=inline
    hash: str            # MD5 hash for deduplication
```

#### `StyleRegistry`
- Tracks which styles have been loaded via hash
- Prevents duplicate styles in the same document
- Returns all styles sorted by priority

#### `StyleCollector`
- One instance per parser render call
- Collects styles from all blocks
- Outputs grouped `<style>` tag at end

### Benefits

**Before (inline styles):**
```html
<div class="sb-alert">...</div>
<style>/* alert styles */</style>

<div class="sb-alert">...</div>
<style>/* same alert styles again! */</style>

<div class="sb-card">...</div>
<style>/* card styles */</style>
```

**After (collected styles):**
```html
<div class="sb-alert">...</div>
<div class="sb-alert">...</div>
<div class="sb-card">...</div>

<style>
/* alert */
.sb-alert { ... }

/* card */
.sb-card { ... }
</style>
```

### Advantages

1. **No Duplication** - Same block used 100 times = styles loaded once
2. **Better Performance** - Single `<style>` tag at end, browser caches better
3. **Clean HTML** - Block templates contain only structure, no styling
4. **Easy Debugging** - All styles in one place at document end
5. **Priority Control** - Builtins load first, user styles can override
6. **Hash-Based** - Identical CSS = same hash = deduplicated automatically

### How It Works

1. **Parse markdown** - Parser splits by code fences
2. **Process SpellBlocks** - Each block encountered:
   - Calls `block.get_styles()` to get CSS
   - Adds to `StyleCollector` with block name and priority
   - Collector checks hash, skips if duplicate
   - Renders block HTML (without inline styles)
3. **Finish rendering** - Apply markdown processing
4. **Append styles** - `StyleCollector.render()` creates final `<style>` tag
5. **Return HTML** - Complete document with deduplicated styles at end

### Disable Style Collection

For special cases (testing, SSG with separate CSS files):

```python
parser = SpellbookParser(collect_styles=False)
html = parser.render(markdown_text)
# No styles appended, blocks render without styling
```

### Future Enhancements

- **Extract to file**: Option to write styles to separate `.css` file
- **Minification**: Compress CSS for production
- **Theming**: CSS variables for easy theme customization
- **Scoped styles**: Shadow DOM for complete isolation