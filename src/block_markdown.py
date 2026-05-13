from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    lines = block.split("\n")

    # heading
    if (
        block.startswith("# ")
        or block.startswith("## ")
        or block.startswith("### ")
        or block.startswith("#### ")
        or block.startswith("##### ")
        or block.startswith("###### ")
    ):
        return BlockType.HEADING

    # code
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    # quote
    is_quote = True
    for line in lines:
        if not line.startswith(">"):
            is_quote = False
            break

    if is_quote:
        return BlockType.QUOTE

    # unordered list
    is_unordered = True
    for line in lines:
        if not line.startswith("- "):
            is_unordered = False
            break

    if is_unordered:
        return BlockType.UNORDERED_LIST

    # ordered list
    is_ordered = True
    for i in range(len(lines)):
        if not lines[i].startswith(f"{i + 1}. "):
            is_ordered = False
            break

    if is_ordered:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH