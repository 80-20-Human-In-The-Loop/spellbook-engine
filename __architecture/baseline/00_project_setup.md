# Project Setup - Spellbook Engine

**Date**: 2025-09-29
**Status**: Baseline
**Version**: 0.1.0

## Overview

Spellbook Engine is a framework-agnostic markdown parser with reusable HTML/Python components called "SpellBlocks". It extends standard markdown with custom component syntax `{~ blockname ~}...{~~}` that renders to HTML using Jinja2 templates.

### Core Philosophy
- **Framework Agnostic**: No hard dependencies on Django, Flask, or any web framework
- **Convention Over Configuration**: Smart defaults with escape hatches
- **Compassionate Error Handling**: Educational, guidance-oriented error messages
- **Progressive Disclosure**: Simple API surface, advanced features when needed

## Project Structure

```
spellbook-engine/
├── __architecture/          # Architecture documentation
│   └── baseline/
│       └── 00_project_setup.md
├── spellbook_engine/        # Main package
│   ├── __init__.py         # Package exports
│   ├── base_block.py       # BaseSpellBlock class
│   ├── registry.py         # SpellBlockRegistry for discovery
│   ├── parser.py           # SpellbookParser for markdown processing
│   ├── exceptions.py       # Custom exceptions
│   └── builtins/           # Built-in SpellBlocks
│       ├── logic/          # Python logic classes
│       │   ├── alert.py
│       │   ├── card.py
│       │   ├── quote.py
│       │   └── render_error.py
│       └── templates/      # Jinja2 templates
│           ├── alert.html
│           ├── card.html
│           ├── quote.html
│           └── render_error.html
├── tests/
│   ├── conftest.py         # Root fixtures
│   ├── unit/               # Unit tests (82 tests)
│   │   ├── test_base_block.py
│   │   ├── test_builtin_blocks.py
│   │   ├── test_exceptions.py
│   │   └── test_registry_discovery.py
│   ├── integration/        # Integration tests (17 tests)
│   │   ├── conftest.py
│   │   └── test_parser_integration.py
│   ├── _dummy_files/       # Test markdown files
│   │   ├── basic_markdown.md
│   │   ├── spellblocks_only.md
│   │   ├── code_heavy.md
│   │   └── edge_cases.md
│   └── _golden_files/      # Expected HTML output
│       ├── basic_markdown.html
│       ├── spellblocks_only.html
│       ├── code_heavy.html
│       └── edge_cases.html
├── CLAUDE.md               # Project constitution & AI agent guidelines
├── pyproject.toml          # Project metadata & tool configs
├── requirements.txt        # Production dependencies
├── requirements-dev.txt    # Development dependencies
└── .pre-commit-config.yaml # Pre-commit hooks config
```

## Core Components

### 1. BaseSpellBlock (`base_block.py`)

Abstract base class for all SpellBlocks.

**Key Features:**
- Automatic markdown processing in `process_content()`
- Template rendering via Jinja2
- Extensible through inheritance
- Context generation for template variables

**Usage Pattern:**
```python
class CustomBlock(BaseSpellBlock):
    def get_context(self) -> dict[str, Any]:
        return {
            "title": self.kwargs.get("title", ""),
            "content": self.process_content(),
        }
```

### 2. SpellBlockRegistry (`registry.py`)

Manages SpellBlock discovery and instantiation.

**Discovery Methods:**
1. **Standard Structure**: `spellblocks/` with `templates/` and `logic/` subdirectories
2. **Flat Structure**: Block name matches file names (e.g., `alert.html` + `alert.py`)
3. **Manual Dictionary**: Explicit registration with paths
4. **Built-ins**: Always loaded unless `load_builtins=False`

**Key Features:**
- Template override system (user templates searched before built-ins)
- Dynamic class loading from Python modules
- Multiple template directory support via `ChoiceLoader`

### 3. SpellbookParser (`parser.py`)

Processes markdown with embedded SpellBlocks.

**Processing Pipeline:**
1. Split content by code fences (protect code blocks)
2. Detect malformed blocks and render errors
3. Process self-closing blocks: `{~ block /~}`
4. Process content blocks: `{~ block ~}...{~~}`
5. Recursively process nested SpellBlocks
6. Apply markdown extensions
7. Return final HTML

**Key Features:**
- Recursive nested SpellBlock support
- Code fence protection
- Compassionate error rendering via `RenderErrorBlock`
- Configurable markdown extensions

## Built-in SpellBlocks

### 1. AlertBlock
Notification messages with type variants (info, warning, danger, success).

**Attributes:**
- `type`: Alert variant
- `title`: Optional heading
- `dismissible`: Boolean for close button

### 2. CardBlock
Content cards with optional header and footer.

**Attributes:**
- `title`: Card header
- `footer`: Card footer
- `style`: Style variant (default, primary, etc.)
- `collapsible`: Boolean for collapse functionality
- `collapsed`: Initial collapsed state

### 3. QuoteBlock
Blockquotes with attribution.

**Attributes:**
- `author`: Quote author
- `source`: Source (book, article, etc.)
- `cite`: URL citation
- `style`: Quote style (default, italic, large)

### 4. RenderErrorBlock (New!)
Compassionate error messages for malformed SpellBlocks.

**Error Types:**
- `unclosed_block`: Missing closing tag `{~~}`
- `orphaned_closing`: Closing tag without opening
- `block_not_found`: SpellBlock name doesn't exist
- `render_exception`: Error during rendering

**Features:**
- Educational error messages with icons (⚠️, ❓, ❌)
- Specific fix suggestions with 💡
- Technical details in collapsible section
- Link to documentation
- Beautiful amber/yellow color scheme (not harsh red)

## Development Setup

### Dependencies

**Production (`requirements.txt`):**
```
markdown>=3.4
Jinja2>=3.0
```

**Development (`requirements-dev.txt`):**
```
pytest>=7.0
pytest-cov>=3.0
storm-checker
ruff>=0.1.0
black>=22.0
flake8>=4.0
mypy>=1.0
pre-commit>=3.0
```

### Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

### Pre-commit Hooks

Configured in `.pre-commit-config.yaml`:
- **black** (v24.10.0): Code formatting
- **ruff** (v0.8.4): Linting and auto-fixing
- **ruff-format**: Code formatting
- **mypy** (v1.13.0): Type checking with strict mode

## Testing Infrastructure

### Test Suite Overview

**Total Tests**: 99 (82 unit + 17 integration)
**Coverage**: 94%
**Execution Time**: ~0.6s

### Unit Tests (82 tests)

#### `test_base_block.py` (17 tests)
- Initialization with defaults, content, template, kwargs
- Context generation and markdown processing
- Template rendering with error handling
- Process method and chaining
- Custom SpellBlock inheritance

#### `test_builtin_blocks.py` (23 tests)
- CardBlock: attributes, rendering, content stripping
- QuoteBlock: attributes, rendering, content processing
- AlertBlock: type variants, attributes, rendering
- Built-in integration tests

#### `test_exceptions.py` (15 tests)
- Exception hierarchy (SpellbookError base)
- SpellBlockDiscoveryError with helpful messages
- SpellBlockLoadError and SpellBlockRenderError
- ParserError handling

#### `test_registry_discovery.py` (27 tests)
- Registry initialization with/without builtins
- Standard structure discovery
- Flat structure discovery
- Manual dictionary configuration
- Error handling for missing/invalid blocks
- Template override system
- Edge cases (file vs directory, hybrid configs)

### Integration Tests (17 tests)

#### Golden File Testing
Uses `SPELLBOOK_UPDATE_GOLDEN=1` environment variable to regenerate expected output.

**Test Files:**
1. `basic_markdown.md`: Comprehensive markdown features + SpellBlocks
2. `spellblocks_only.md`: Focus on SpellBlock rendering
3. `code_heavy.md`: Code fence protection verification
4. `edge_cases.md`: Malformed blocks, nested blocks, unicode, etc.

**Test Categories:**
- Basic markdown parsing
- SpellBlocks-only documents
- Code block protection
- Edge cases (empty blocks, malformed syntax, unicode)
- Parser configuration
- Markdown features (headings, lists, code, links, emphasis)
- SpellBlock/markdown interaction

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=spellbook_engine --cov-report=term-missing

# Run specific test file
pytest tests/unit/test_base_block.py -xvs

# Update golden files
SPELLBOOK_UPDATE_GOLDEN=1 pytest tests/integration/

# Run tests in parallel (if pytest-xdist installed)
pytest -n auto
```

## Configuration Files

### `pyproject.toml`

**Project Metadata:**
- Name: spellbook-engine
- Python version: >=3.10
- License: MIT

**Tool Configurations:**

**Ruff:**
```toml
[tool.ruff]
line-length = 88
target-version = "py310"

[tool.ruff.lint]
select = ["E", "W", "F", "I", "N", "UP", "B", "C4", "SIM"]
known-first-party = ["spellbook_engine"]
```

**Mypy:**
```toml
[tool.mypy]
python_version = "3.10"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

## Key Design Decisions

### 1. Markdown Processing in BaseSpellBlock

**Decision**: All SpellBlocks automatically process markdown in `process_content()`.

**Rationale**:
- Enables rich formatting inside components
- Consistent behavior across all blocks
- Override via inheritance for special cases

**Implementation**:
```python
def process_content(self) -> str:
    if not self.content:
        return ""
    return markdown.markdown(
        self.content.strip(),
        extensions=["markdown.extensions.fenced_code", "markdown.extensions.nl2br"],
    ).strip()
```

### 2. Nested SpellBlock Support

**Decision**: SpellBlocks can be nested recursively.

**Rationale**:
- Enables complex layouts (alerts inside cards, etc.)
- Natural composition pattern
- Matches user expectations

**Implementation**: Recursive call to `_process_spellblocks()` in `_render_spellblock()`.

### 3. Compassionate Error Rendering

**Decision**: Errors render as beautiful, educational SpellBlocks instead of HTML comments.

**Rationale**:
- Users need guidance, not cryptic errors
- Visual errors are easier to spot in rendered output
- Maintains HTML validity
- Provides actionable fix suggestions

**Features**:
- Friendly error messages with emoji icons
- Specific suggestions (e.g., "Add `{~~}` after your content")
- Technical details in collapsible section
- Warm color scheme (amber/yellow, not red)
- Links to documentation

### 4. Template Override System

**Decision**: User templates searched before built-in templates.

**Rationale**:
- Allows customization without modifying source
- Standard pattern in template engines
- Maintains backward compatibility

**Implementation**: Reverse directory list in `ChoiceLoader`.

### 5. Code Fence Protection

**Decision**: Protect code blocks from SpellBlock processing.

**Rationale**:
- SpellBlock syntax in code examples should be literal
- Prevents unintended rendering
- Standard markdown parser behavior

**Implementation**: Split content by `^```` pattern, skip processing for code segments.

## Quality Metrics

**Test Coverage**: 94%
**Uncovered Lines**:
- `parser.py`: 13 lines (87% coverage)
  - Exception handling edge cases
  - Logging statements
- `registry.py`: 6 lines (96% coverage)
  - Error handling paths

**Code Quality Tools**:
- Ruff: No violations
- Black: All files formatted
- Mypy: Strict type checking passing
- Flake8: Passing

## Next Steps / Future Enhancements

1. **Documentation**:
   - User guide with examples
   - API reference
   - Contributing guidelines

2. **Additional Built-ins**:
   - TabsBlock for tabbed content
   - AccordionBlock for collapsible sections
   - CodeBlock with syntax highlighting
   - ImageBlock with captions

3. **Performance**:
   - Caching for template compilation
   - Lazy loading of built-in blocks
   - Benchmark suite

4. **Features**:
   - Self-closing blocks with content via attributes
   - SpellBlock composition/inheritance
   - Custom markdown extensions per block
   - Asset bundling (CSS/JS)

5. **Testing**:
   - Browser-based visual regression tests
   - Performance benchmarks
   - Fuzzing for edge cases

## References

- **CLAUDE.md**: Project constitution and AI agent guidelines
- **Python-Markdown**: https://python-markdown.github.io/
- **Jinja2**: https://jinja.palletsprojects.com/
- **Pytest**: https://docs.pytest.org/

---

**Last Updated**: 2025-09-29
**Next Review**: When adding major features or architectural changes