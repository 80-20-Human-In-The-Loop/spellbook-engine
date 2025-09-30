# SpellBlocks Only Test

This file focuses on testing SpellBlock rendering with minimal markdown.

{~ alert type="info" ~}
This is an info alert.
{~~}

{~ alert type="success" ~}
Operation completed successfully!
{~~}

{~ alert type="warning" ~}
Warning: Please be careful with this operation.
{~~}

{~ alert type="danger" ~}
Error: Something went wrong!
{~~}

{~ card title="Simple Card" ~}
This is a simple card with just a title.
{~~}

{~ card title="Full Card" footer="Last updated: 2025" ~}
This card has both a title and a footer.

It can contain multiple paragraphs.

And even **formatted** text!
{~~}

{~ quote author="Albert Einstein" ~}
Imagination is more important than knowledge.
{~~}

{~ quote author="Steve Jobs" source="Stanford Speech" cite="https://example.com" ~}
Stay hungry, stay foolish.
{~~}

{~ card title="Nested Content" ~}
Cards can contain other markdown:

- List item 1
- List item 2
- List item 3

And even code: `inline_code()`
{~~}

{~ card title="Collapsible Card" collapsible="true" ~}
This card has a collapse button in the header!

Click the button to collapse/expand the content.
{~~}

{~ card title="Initially Collapsed Card" collapsible="true" collapsed="true" ~}
This card starts collapsed and can be expanded.

The content is hidden by default!
{~~}

{~ card title="Primary Style Card" style="primary" ~}
This card uses the primary style variant with blue header.
{~~}

{~ card title="Secondary Style Card" style="secondary" ~}
This card uses the secondary style variant with gray header.
{~~}