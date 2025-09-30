# Complete Markdown Test Document

This document contains **all** the markdown features to test the spellbook-engine parser.

## Headings

### Level 3 Heading
#### Level 4 Heading
##### Level 5 Heading
###### Level 6 Heading

## Text Formatting

This is **bold text** and this is __also bold__.

This is *italic text* and this is _also italic_.

This is ***bold and italic*** combined.

This is ~~strikethrough~~ text.

This is `inline code` in a sentence.

## Lists

### Unordered Lists

- First item
- Second item
  - Nested item 1
  - Nested item 2
    - Deeply nested item
- Third item

### Ordered Lists

1. First step
2. Second step
   1. Sub-step A
   2. Sub-step B
3. Third step

### Task Lists

- [x] Completed task
- [ ] Incomplete task
- [ ] Another incomplete task

## Links and Images

This is a [link to Anthropic](https://www.anthropic.com).

This is a [link with title](https://example.com "Example Domain").

Reference-style links: [See this reference][ref1]

[ref1]: https://docs.python.org "Python Documentation"

Images work similarly: ![Alt text](https://via.placeholder.com/150)

## Blockquotes

> This is a blockquote.
> It can span multiple lines.
>
> And multiple paragraphs.

> Nested blockquotes:
> > This is nested
> > > And this is deeply nested

## Code Blocks

### Inline Code

Use the `print()` function to output text.

### Fenced Code Block (Python)

```python
def hello_world():
    """A simple function."""
    message = "Hello, World!"
    print(message)
    return True

class SpellBlock:
    def __init__(self, name):
        self.name = name
```

### Fenced Code Block (JavaScript)

```javascript
function greet(name) {
  console.log(`Hello, ${name}!`);
  return {
    success: true,
    message: "Greeted successfully"
  };
}

const result = greet("Developer");
```

### Fenced Code Block (Bash)

```bash
#!/bin/bash
echo "Running tests..."
pytest tests/ --cov=spellbook_engine
echo "Tests complete!"
```

### Code Block with No Language

```
This is a plain code block
  with indentation preserved
  and no syntax highlighting
```

## Tables

| Feature | Supported | Notes |
|---------|-----------|-------|
| Headers |  | All levels 1-6 |
| Lists |  | Ordered, unordered, nested |
| Code blocks |  | Fenced and indented |
| SpellBlocks |  | Custom syntax |

Alignment options:

| Left Aligned | Center Aligned | Right Aligned |
|:------------|:--------------:|--------------:|
| Left | Center | Right |
| A | B | C |

## Horizontal Rules

Three or more hyphens:

---

Three or more asterisks:

***

Three or more underscores:

___

## Emphasis and Combinations

*You can combine **bold** inside italic.*

**You can combine *italic* inside bold.**

***You can have both bold and italic.***

## Line Breaks

This line ends with two spaces
And continues here on a new line.

You can also use a backslash\
for a line break.

## Footnotes

Here's a sentence with a footnote[^1].

Here's another with a longer footnote[^longnote].

[^1]: This is the first footnote.

[^longnote]: Here's one with multiple paragraphs.

    Indent paragraphs to include them in the footnote.

    You can add as many as you need.

## Escaping Characters

You can escape special characters with backslash:

\* Not italic \*

\# Not a heading

\[Not a link\](nowhere)

## HTML in Markdown

You can also use <strong>HTML tags</strong> directly.

<div class="custom-class">
  <p>This is an HTML block.</p>
</div>

## Definition Lists

Term 1
: Definition 1

Term 2
: Definition 2a
: Definition 2b

## Abbreviations

The HTML specification is maintained by the W3C.

*[HTML]: Hyper Text Markup Language
*[W3C]: World Wide Web Consortium

## Attributes (with attr_list extension)

### Heading with ID {#custom-id}

Paragraph with custom class {.custom-class}

### Link with Attributes

[Link with attributes](https://example.com){:target="_blank" .external}

## Complex Nested Structure

1. First ordered item
   - Nested unordered item
     > With a blockquote
     > ```python
     > code = "inside blockquote"
     > ```
   - Another nested item
2. Second ordered item
   - More nesting
     1. Ordered inside unordered
     2. Another ordered item

## SpellBlocks Examples

{~ alert type="info" ~}
This is an informational alert with **markdown** support!
{~~}

{~ card title="Welcome Card" footer="Updated 2025" ~}
This is a card with a title and footer.

It can contain:
- Multiple paragraphs
- **Formatted text**
- And other markdown

{~~}

{~ quote author="Albert Einstein" source="Physics Journal" ~}
Imagination is more important than knowledge.
{~~}

## Mixed Content

Here's a paragraph followed by code:

```python
def complex_example():
    # This is preserved even though
    # there are SpellBlocks nearby
    return "Works correctly"
```

And here's a SpellBlock after code:

{~ alert type="success" ~}
Code blocks and SpellBlocks don't interfere with each other!
{~~}

More text here.

## Edge Cases

Empty emphasis: ** **

Multiple spaces    between    words.

Trailing spaces at end of line:

## Final Section

This document tests comprehensive markdown parsing including:

1. All standard markdown syntax
2. Code blocks that should be protected
3. SpellBlocks that should be processed
4. Nested structures
5. Edge cases

**End of test document.**