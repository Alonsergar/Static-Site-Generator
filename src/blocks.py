from enum import Enum
from inline import text_to_textnodes
from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import text_node_to_html_node, TextNode, TextType


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    for i in range(0, len(blocks)):
        blocks[i] = blocks[i].strip()
    blocks = [x for x in blocks if x != ""]
    return blocks


def block_to_block_type(block: str):
    if block.startswith("#"):
        count = len(block) - len(block.lstrip("#"))
        if 1 <= count <= 6 and block[count] == " ":
            return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    lines = block.split("\n")
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    expected = 1
    is_ordered = True
    for line in lines:
        prefix = f"{expected}. "
        if not line.startswith(prefix):
            is_ordered = False
            break
        expected += 1
    if is_ordered:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def text_to_children(text):
    textnodes = text_to_textnodes(text)
    children = []
    for node in textnodes:
        children.append(text_node_to_html_node(node))
    return children


def heading_to_html_node(block):
    count = len(block) - len(block.lstrip("#"))
    text = block[count + 1:]
    return ParentNode(tag=f"h{count}", children=text_to_children(text))


def code_to_html_node(block):
    # Strip the ``` fences; preserve inner content exactly
    text = block[3:]  # remove leading ```
    if text.startswith("\n"):
        text = text[1:]
    if text.endswith("```"):
        text = text[:-3]
    code_node = LeafNode("code", text)
    return ParentNode(tag="pre", children=[code_node])


def quote_to_html_node(block):
    lines = block.split("\n")
    stripped = "\n".join(line.lstrip(">").lstrip(" ") for line in lines)
    return ParentNode(tag="blockquote", children=text_to_children(stripped))


def unordered_list_to_html_node(block):
    lines = block.split("\n")
    items = []
    for line in lines:
        text = line[2:]  # remove "- "
        items.append(ParentNode(tag="li", children=text_to_children(text)))
    return ParentNode(tag="ul", children=items)


def ordered_list_to_html_node(block):
    lines = block.split("\n")
    items = []
    for i, line in enumerate(lines):
        text = line[len(f"{i+1}. "):]
        items.append(ParentNode(tag="li", children=text_to_children(text)))
    return ParentNode(tag="ol", children=items)


def paragraph_to_html_node(block):
    # Replace newlines with spaces for inline content
    text = " ".join(block.split("\n"))
    return ParentNode(tag="p", children=text_to_children(text))


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes_blocks = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.HEADING:
            node = heading_to_html_node(block)
        elif block_type == BlockType.CODE:
            node = code_to_html_node(block)
        elif block_type == BlockType.QUOTE:
            node = quote_to_html_node(block)
        elif block_type == BlockType.UNORDERED_LIST:
            node = unordered_list_to_html_node(block)
        elif block_type == BlockType.ORDERED_LIST:
            node = ordered_list_to_html_node(block)
        elif block_type == BlockType.PARAGRAPH:
            node = paragraph_to_html_node(block)
        else:
            raise Exception("Invalid blockType")

        html_nodes_blocks.append(node)

    return ParentNode(tag="div", children=html_nodes_blocks)