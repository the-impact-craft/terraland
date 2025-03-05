from secrets import choice

NAME = "TerraLand"

BASE_FRAME = r"""
              ,---------------------------,
              |  /---------------------\  |
              | |                       | |
              | |                       | |
              | |       {}              | |
              | |                       | |
              | |                       | |
              |  \_____________________/  |
              |___________________________|
            ,---\_____     []     _______/------,
          /         /______________\           /|
        /___________________________________ /  | ___
        |                                   |   |    )
        |  _ _ _                 [-------]  |   |   (
        |  o o o                 [-------]  |  /    _)_
        |__________________________________ |/     /  /
    /-------------------------------------/|      ( )/
  /-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/ /
/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/ /
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


def build_animation_frames(text):
    """
    Build animation frames

    Args:
        text: The text to animate
    """
    result = []
    key_board_lines = []
    keyword_symbols = "/-" * 10

    for index, row in enumerate(BASE_FRAME.split("\n")):
        if keyword_symbols in row:
            key_board_lines.append(index)
        if "{}" in row:
            placeholder_index = row.index("{}")
            row = row[:placeholder_index] + text + row[placeholder_index + len(text) :]
        result.append(row)

    if not key_board_lines:
        return "\n".join(result)

    random_keyboard_line_index = choice(key_board_lines)
    random_keyboard_line = list(result[random_keyboard_line_index])
    key_indexes = [i for i, char in enumerate(random_keyboard_line) if char == "-"]
    random_keyboard_line[choice(key_indexes)] = "_"
    result[random_keyboard_line_index] = "".join(random_keyboard_line)

    return "\n".join(result)

LOGO_ANIMATION = [
    build_animation_frames(placeholder)
    for placeholder in 
    [f"${NAME[:i]}_" for i in range(len(NAME)+1)]
]
