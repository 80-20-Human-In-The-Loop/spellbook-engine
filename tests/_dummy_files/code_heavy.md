# Code-Heavy Test Document

This file tests that code blocks are properly protected from SpellBlock processing.

## Python Code Block

```python
def process_spellblock(content):
    """
    This function mentions {~ alert ~} but it's in a code block
    so it should NOT be processed.
    """
    # Even mentions like {~ card title="test" ~} should be preserved
    return content.strip()

class Parser:
    def render(self):
        # This {~~} closing tag should also be preserved
        return "{~ This is not processed ~}"
```

## JavaScript with SpellBlock Syntax

```javascript
const spellblock = "{~ alert type='info' ~}";
const closing = "{~~}";

// These should NOT be turned into actual SpellBlocks
function testParser() {
  const test = `
    {~ card title="Test" ~}
    Content here
    {~~}
  `;
  return test;
}
```

## Bash Scripts

```bash
#!/bin/bash
# Script that echoes SpellBlock-like syntax
echo "{~ alert type='warning' ~}"
echo "Processing..."
echo "{~~}"
```

## Inline Code

Use `{~ alert ~}` to create an alert. Close it with `{~~}`.

The syntax is: `{~ blockname attribute="value" ~}content{~~}`

## Mixed Content - Code and SpellBlocks

Here's some text before code:

```python
def example():
    # This {~ should not process ~}
    return True
```

Now a real SpellBlock after the code:

{~ alert type="success" ~}
Code blocks are properly protected!
{~~}

More code:

```python
another_code = "{~ fake spellblock ~}"
```

And another real SpellBlock:

{~ card title="Real Card" ~}
This card should render, but the code blocks above should preserve their SpellBlock syntax.
{~~}

## Edge Case: SpellBlock Immediately After Code

```python
code = "test"
```
{~ alert type="info" ~}
This alert comes right after a code block.
{~~}

## Plain Text Code Block

```
{~ This looks like a SpellBlock ~}
But it's in a plain code block
{~~}
```

## Indented Code (Markdown Style)

    {~ alert ~}
    This is indented code
    {~~}

Should the above be processed? Let's test!

{~ quote author="Test" ~}
Real SpellBlocks still work outside code blocks.
{~~}