# Spellbook Engine

> A framework-agnostic markdown parser with reusable HTML/Python components

[![Tests](https://img.shields.io/badge/tests-99%20passing-brightgreen)](tests/)
[![Coverage](https://img.shields.io/badge/coverage-94%25-brightgreen)](tests/)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](pyproject.toml)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

Spellbook Engine extends standard markdown with custom component syntax `{~ blockname ~}...{~~}` that renders to beautiful HTML using Jinja2 templates. Think of it as markdown with superpowers! ✨

## Features

- 🎯 **Framework Agnostic** - Works with Django, Flask, FastAPI, or standalone
- 🧩 **Component-Based** - Self-contained HTML/Python pairs (SpellBlocks)
- 🪆 **Nested Support** - SpellBlocks can contain other SpellBlocks
- 📝 **Markdown Inside** - Full markdown support within components
- 💡 **Compassionate Errors** - Beautiful, educational error messages with fix suggestions
- 🔒 **Code Protection** - Code fences are automatically protected from processing
- 🎨 **Customizable** - Create your own SpellBlocks or override built-ins

## Installation

```bash
# From PyPI (when published)
pip install spellbook-engine

# From source
git clone https://github.com/yourusername/spellbook-engine.git
cd spellbook-engine
pip install -e .
```

## Quick Start

```python
from spellbook_engine import SpellbookParser

# Create parser with built-in SpellBlocks
parser = SpellbookParser()

# Parse markdown with SpellBlocks
markdown_text = """
# Hello World

{~ alert type="info" ~}
This is an **informational** alert with markdown support!
{~~}

{~ card title="Welcome" ~}
Cards can contain:
- Multiple paragraphs
- **Formatted text**
- And even nested SpellBlocks!
{~~}
"""

html = parser.render(markdown_text)
print(html)
```

## SpellBlock Syntax

### Content Blocks

```markdown
{~ blockname attribute="value" ~}
Content goes here with **markdown** support!
{~~}
```

### Self-Closing Blocks

```markdown
{~ blockname attribute="value" /~}
```

### Nested Blocks

```markdown
{~ card title="Outer Card" ~}
This is the outer content.

{~ alert type="warning" ~}
This alert is nested inside the card!
{~~}

More outer content here.
{~~}
```

## Built-in SpellBlocks

### Alert

Display notification messages with different types.

```markdown
{~ alert type="info" ~}
This is an informational message.
{~~}

{~ alert type="warning" title="Warning!" ~}
Be careful with this operation.
{~~}

{~ alert type="success" ~}
Operation completed successfully!
{~~}
```

**Attributes:**
- `type`: `info`, `warning`, `danger`, `success` (default: `info`)
- `title`: Optional heading
- `dismissible`: Boolean for close button

### Card

Display content in a card layout with optional header and footer.

```markdown
{~ card title="Card Title" footer="Last updated: 2025" ~}
This is the card body content.

It can contain **multiple paragraphs** and markdown!
{~~}
```

**Attributes:**
- `title`: Card header text
- `footer`: Card footer text
- `style`: `default`, `primary`, `secondary`, etc.
- `collapsible`: Boolean for collapse functionality
- `collapsed`: Initial collapsed state

### Quote

Display blockquotes with attribution.

```markdown
{~ quote author="Albert Einstein" source="Physics Journal" ~}
Imagination is more important than knowledge.
{~~}
```

**Attributes:**
- `author`: Quote author
- `source`: Source (book, article, etc.)
- `cite`: URL citation
- `style`: `default`, `italic`, `large`

## Creating Custom SpellBlocks

### 1. Create the Template

Create `myblocks/templates/highlight.html`:

```html
<div class="highlight highlight-{{ color }}">
    <div class="highlight-content">
        {{ content }}
    </div>
</div>
```

### 2. Create the Logic Class

Create `myblocks/logic/highlight.py`:

```python
from typing import Any
from spellbook_engine import BaseSpellBlock

class HighlightBlock(BaseSpellBlock):
    """Highlight block with color variants."""

    def get_context(self) -> dict[str, Any]:
        return {
            "color": self.kwargs.get("color", "yellow"),
            "content": self.process_content(),
        }
```

### 3. Register and Use

```python
from spellbook_engine import SpellbookParser, SpellBlockRegistry

# Register your custom blocks
registry = SpellBlockRegistry()
registry.discover("./myblocks")

# Create parser with custom blocks
parser = SpellbookParser(registry=registry)

# Use your custom block
markdown = """
{~ highlight color="blue" ~}
This text will be highlighted in **blue**!
{~~}
"""

html = parser.render(markdown)
```

## Advanced Features

### Markdown Processing

All SpellBlocks automatically process markdown in their content:

```markdown
{~ card title="Rich Content" ~}
# Heading inside card

**Bold** and *italic* text, plus:
- Lists
- `inline code`
- [Links](https://example.com)

```python
# Even code blocks!
def hello():
    return "world"
```
{~~}
```

### Compassionate Error Messages

When you make a mistake, Spellbook Engine provides helpful, educational error messages:

```markdown
{~ alert type="info" ~}
Oops, I forgot the closing tag!
```

Renders as a beautiful error block with:
- ⚠️ Clear error type and message
- 💡 Specific fix suggestion
- 📚 Link to documentation
- Warm, friendly color scheme (not scary red!)

### Code Fence Protection

Code examples are automatically protected from SpellBlock processing:

````markdown
Here's how to use an alert:

```markdown
{~ alert type="info" ~}
This syntax is protected and won't render!
{~~}
```

But this one will render:
{~ alert type="info" ~}
This is a real alert!
{~~}
````

## Development

### Running Tests

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=spellbook_engine --cov-report=term-missing

# Run specific test file
pytest tests/unit/test_base_block.py -xvs
```

### Pre-commit Hooks

```bash
# Install pre-commit hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

The project uses:
- **black**: Code formatting
- **ruff**: Linting and auto-fixing
- **mypy**: Type checking (strict mode)

### Test Suite

- **99 tests** (82 unit + 17 integration)
- **94% coverage**
- **Golden file testing** for integration tests
- **~0.6s execution time**

## Project Structure

```
spellbook-engine/
├── spellbook_engine/        # Main package
│   ├── base_block.py        # BaseSpellBlock class
│   ├── registry.py          # SpellBlock discovery & registration
│   ├── parser.py            # Markdown parser with SpellBlock support
│   ├── exceptions.py        # Custom exceptions
│   └── builtins/            # Built-in SpellBlocks
│       ├── logic/           # Python classes
│       └── templates/       # Jinja2 templates
├── tests/                   # Test suite
│   ├── unit/               # Unit tests
│   ├── integration/        # Integration tests with golden files
│   ├── _dummy_files/       # Test markdown files
│   └── _golden_files/      # Expected HTML output
├── __architecture/         # Architecture documentation
│   └── baseline/
│       └── 00_project_setup.md
├── CLAUDE.md              # Project constitution & guidelines
├── README.md              # This file
├── pyproject.toml         # Project metadata & tool configs
└── requirements*.txt      # Dependencies
```

## Documentation

- **Architecture Docs**: [`__architecture/baseline/00_project_setup.md`](__architecture/baseline/00_project_setup.md)
- **Project Constitution**: [`CLAUDE.md`](CLAUDE.md)
- **API Reference**: Coming soon!
- **Examples & Guides**: Coming soon!

## Philosophy

Spellbook Engine follows these core principles:

- **Framework Agnostic** - No hard dependencies on web frameworks
- **Convention Over Configuration** - Smart defaults with escape hatches
- **Progressive Disclosure** - Simple API surface, advanced features when needed
- **Compassionate** - Helpful error messages that guide users to solutions
- **Composable** - Small focused components over monolithic systems

See [`CLAUDE.md`](CLAUDE.md) for the complete architectural philosophy and decision principles.

## Contributing

We welcome contributions! Here's how you can help:

1. **Report bugs** - Open an issue with a clear description and minimal reproduction
2. **Suggest features** - Discuss new ideas in issues before implementing
3. **Improve docs** - Fix typos, add examples, clarify explanations
4. **Write tests** - Increase coverage, add edge cases
5. **Create SpellBlocks** - Share your custom blocks with the community!

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Install pre-commit hooks (`pre-commit install`)
4. Make your changes with tests
5. Run the test suite (`pytest`)
6. Commit your changes (pre-commit will run automatically)
7. Push to your fork and create a Pull Request

## Roadmap

- [ ] Publish to PyPI
- [ ] User guide with comprehensive examples
- [ ] API reference documentation
- [ ] Additional built-in blocks (Tabs, Accordion, Code with syntax highlighting)
- [ ] Performance optimizations (template caching, lazy loading)
- [ ] Visual regression tests
- [ ] CLI tool for rendering markdown files

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Credits

Created by [Mathew Storm](https://github.com/yourusername) as an extraction from Django-Spellbook to make markdown component magic accessible to all Python web frameworks.

Special thanks to:
- The Python-Markdown team for the excellent markdown library
- The Jinja2 team for the powerful templating engine
- All contributors who help make this project better!

---

**Made with ✨ and a bit of markdown magic**