from parentnode import ParentNode
from leafnode import LeafNode
from textnode import text_node_to_html_node
from textnode import TextNode, TextType

from markdown_blocks import markdown_to_blocks
from block_markdown import BlockType, block_to_block_type
from inline_markdown import text_to_textnodes


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []

    for node in text_nodes:
        children.append(text_node_to_html_node(node))

    return children


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            paragraph = block.replace("\n", " ")
            node = ParentNode("p", text_to_children(paragraph))

        elif block_type == BlockType.HEADING:
            level = 0
            for char in block:
                if char == "#":
                    level += 1
                else:
                    break

            text = block[level + 1 :]
            node = ParentNode(f"h{level}", text_to_children(text))

        elif block_type == BlockType.CODE:
            text = block[4:-3]
            text_node = TextNode(text, TextType.TEXT)
            child = text_node_to_html_node(text_node)

            code_node = ParentNode("code", [child])
            node = ParentNode("pre", [code_node])

        elif block_type == BlockType.QUOTE:
            lines = block.split("\n")
            cleaned = []

            for line in lines:
                cleaned.append(line.lstrip(">").strip())

            content = " ".join(cleaned)
            node = ParentNode("blockquote", text_to_children(content))

        elif block_type == BlockType.UNORDERED_LIST:
            items = []

            for line in block.split("\n"):
                text = line[2:]
                items.append(
                    ParentNode("li", text_to_children(text))
                )

            node = ParentNode("ul", items)

        elif block_type == BlockType.ORDERED_LIST:
            items = []

            for line in block.split("\n"):
                text = line[3:]
                items.append(
                    ParentNode("li", text_to_children(text))
                )

            node = ParentNode("ol", items)

        children.append(node)

    return ParentNode("div", children)