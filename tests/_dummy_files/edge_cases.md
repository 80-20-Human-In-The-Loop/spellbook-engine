# Edge Cases Test Document

This file tests various edge cases and potential issues.

## Empty SpellBlocks

{~ alert ~}
{~~}

{~ card ~}
{~~}

{~ quote ~}
{~~}

## SpellBlocks with Only Whitespace

{~ alert type="info" ~}


{~~}

{~ card title="Empty" ~}


{~~}

## Malformed SpellBlocks (Should Be Ignored or Handled Gracefully)

This has no closing: {~ alert type="info" ~}
This text continues normally.

This has no opening but has closing {~~}

Mismatched: {~ alert ~} content here {~ card ~}

## Nested SpellBlocks (Should Not Be Supported)

{~ card title="Outer" ~}
This is outer content.
{~ alert type="info" ~}
Nested alert?
{~~}
More outer content.
{~~}

## SpellBlocks with Special Characters

{~ alert type="info" ~}
Content with special chars: & < > " ' \n \t
{~~}

{~ card title="Title with \"quotes\" and 'apostrophes'" ~}
Content here.
{~~}

## Multiple SpellBlocks on Same Line

{~ alert ~}First{~~} {~ alert ~}Second{~~}

## SpellBlock Split Across Lines

{~ alert
   type="info"
   ~}
Content split across lines
{~~}

## Empty Attributes

{~ alert type="" ~}
Empty type attribute
{~~}

{~ card title="" footer="" ~}
Empty strings
{~~}

## Very Long Content

{~ card title="Long Content Test" ~}
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.
{~~}

## Unicode Content

{~ alert type="info" ~}
Unicode content: 你好 مرحبا Привет emoji: 🎉 ✨ 🚀
{~~}

{~ quote author="Japanese Proverb" ~}
七転び八起き (Fall seven times, stand up eight)
{~~}

## SpellBlock Followed Immediately by Markdown

{~ alert ~}Alert content{~~}**Bold text** right after

## Markdown Inside SpellBlocks

{~ card title="Markdown Test" ~}
# Heading inside card?
**Bold** and *italic* and `code`

- List item 1
- List item 2

> Blockquote inside card?
{~~}

## Real World Mix

Here's a paragraph with **formatting** and a [link](https://example.com).

{~ alert type="warning" ~}
Warning message here!
{~~}

Another paragraph with `inline code` and more text.

```python
def code_block():
    return "protected"
```

{~ card title="Summary" ~}
Final card with summary.
{~~}

End of document.