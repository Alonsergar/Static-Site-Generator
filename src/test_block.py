import unittest
from blocks import markdown_to_blocks,block_to_block_type,BlockType,markdown_to_html_node

class TestBlockt(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    def test_heading_single_hash(self):
        block = "# Heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)


    def test_heading_six_hashes(self):
        block = "###### Heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)


    def test_heading_with_hash_inside_text(self):
        block = "# Heading with # inside"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)


    def test_heading_no_space_after_hash(self):
        block = "#Heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


    def test_heading_too_many_hashes(self):
        block = "####### Too many"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code_block_simple(self):
        block = "```\ncode here\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)


    def test_code_block_with_markdown_inside(self):
        block = "```\n# not a heading\n- not a list\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)


    def test_code_block_missing_closing(self):
        block = "```\ncode here"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_quote_single_line(self):
        block = "> quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)


    def test_quote_multiline(self):
        block = "> line one\n> line two"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)


    def test_quote_with_space_optional(self):
        block = ">line one\n> line two"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)


    def test_quote_mixed_lines(self):
        block = "> quote\nnormal line"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list_single_item(self):
        block = "- item"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)


    def test_unordered_list_multiple_items(self):
        block = "- item one\n- item two\n- item three"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)


    def test_unordered_list_missing_space(self):
        block = "-item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


    def test_ordered_list_valid(self):
        block = "1. one\n2. two\n3. three"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)


    def test_ordered_list_not_starting_at_one(self):
        block = "2. two\n3. three"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


    def test_ordered_list_not_incrementing(self):
        block = "1. one\n3. three"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


    def test_ordered_list_missing_space(self):
        block = "1.one"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


    def test_plain_paragraph(self):
        block = "This is a normal paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


    def test_paragraph_with_markdown_symbols_inside(self):
        block = "This # is - just > text"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

class TestMarkdownToHtmlNode(unittest.TestCase):

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        md = "## Hello **world**"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h2>Hello <b>world</b></h2></div>")

    def test_quote(self):
        md = "> This is a quote\n> with multiple lines"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>This is a quote\nwith multiple lines</blockquote></div>")

    def test_unordered_list(self):
        md = "- Item one\n- Item **two**\n- Item three"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item one</li><li>Item <b>two</b></li><li>Item three</li></ul></div>",
        )

    def test_ordered_list(self):
        md = "1. First\n2. Second\n3. Third"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First</li><li>Second</li><li>Third</li></ol></div>",
        )

    def test_mixed_blocks(self):
        md = """# Title

A paragraph with _italic_.

- one
- two
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Title</h1><p>A paragraph with <i>italic</i>.</p><ul><li>one</li><li>two</li></ul></div>",
        )
if __name__ == "__main__":
    unittest.main()
