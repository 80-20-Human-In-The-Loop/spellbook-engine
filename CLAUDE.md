# Main Prompt - Spellbook Engine

## Preamble
This document defines the architectural principles and design philosophy for Spellbook Engine - a framework-agnostic markdown parser with reusable HTML/Python components.

### Project: Spellbook Engine
### Philosophy: Simple conventions, flexible discovery, clean separation
### Created: [Date]
### Last Constitutional Review: [Date]

## Constitutional Patterns

### Core Architecture
- **Framework Agnostic**: No hard dependencies on Django, Flask, or any web framework
- **Component-Based**: SpellBlocks are self-contained HTML/Python pairs
- **Convention Over Configuration**: Smart defaults with escape hatches
- **Progressive Disclosure**: Simple API surface, advanced features when needed

### SpellBlock Discovery Hierarchy
1. No args → Check `./spellblocks/` directory
2. Path arg → Check for `templates/` + `logic/` structure
3. Path arg → Fallback to flat structure (`block.html` + `block.py`)
4. Dict arg → Manual registration with explicit paths
5. Not found → Helpful error messages with examples

### Parser Pipeline
1. Protect code fences first
2. Process SpellBlocks in non-code segments
3. Apply markdown extensions
4. Render through templating engine

## Forbidden Anti-Patterns

- **No Framework Lock-in**: Never require Django/Flask/FastAPI specific imports in core
- **No Magic Imports**: All SpellBlock discovery must be explicit and traceable
- **No Silent Failures**: Missing blocks must error with clear guidance
- **No Nested SpellBlock Processing**: Process only top-level blocks to avoid recursion hell
- **No Direct File Writes**: Parser only returns strings, consuming code handles persistence

## Decision Principles

### When Choosing Between Options
- **Explicit > Implicit**: Clear discovery paths over magic
- **Simple > Clever**: Readable code over performance micro-optimizations
- **Helpful > Terse**: Error messages should guide users to solutions
- **Composable > Monolithic**: Small focused functions over god objects

### Extension Points
- Renderers are pluggable (HTML, AST, Debug)
- SpellBlocks are discoverable via multiple methods
- Markdown extensions are configurable
- Template engines are swappable (Jinja2 default)

## Human Agency Requirements

### Requires Human Decision
- Breaking API changes
- New discovery methods
- Default behavior changes
- Security-related modifications

### AI Can Suggest But Not Decide
- Performance optimizations
- New SpellBlock examples
- Documentation improvements
- Test coverage additions

---

*Original Signatories:*

**[Mathew Storm]** [Creator/Founder]: Extracting the parser to make markdown magic accessible everywhere.

---

## Architecture Documentation

### Baseline Documentation
The `__architecture/` directory contains architectural snapshots and decision records. These documents serve as historical baselines for understanding how and why the project evolved.

**Structure:**
- `baseline/`: Architectural snapshots at key milestones
  - `00_project_setup.md`: Initial project structure, components, and design decisions

### When to Update Architecture Docs

**Create New Baseline When:**
- Major architectural changes (new core components, significant refactoring)
- Breaking API changes that alter fundamental usage patterns
- New design patterns or paradigms adopted
- Significant performance or security improvements that change architecture

**DO NOT Update For:**
- Bug fixes
- Minor feature additions
- Documentation improvements
- Test additions
- Dependency updates

### Architecture Review Process
1. Review existing baseline documents before making architectural changes
2. Document new decisions in existing baseline or create new numbered baseline
3. Update CLAUDE.md if constitutional patterns change
4. Link related code changes to architectural decisions

**Current Baseline**: `baseline/00_project_setup.md` (2025-09-29)

---

## Binding Directives for All AI Agents

When contributing to Spellbook Engine, you must:

Type hint for mypy strict mode
Follow ruff standards