from collections import Counter


def format_text(text: str, max_chars_line: int = 40):
    curr_line = ''
    formatted_text = ''
    for token in text.split():
        aux_curr_line = f'{curr_line} {token}' if curr_line else token
        if len(aux_curr_line) <= max_chars_line:
            curr_line = aux_curr_line
            aux_curr_line = ''
        else:
            formatted_text = f'{formatted_text}\n{curr_line}' if formatted_text else curr_line
            curr_line = token
    if not aux_curr_line:
        formatted_text = f'{formatted_text}\n{curr_line}'
    return formatted_text


def format_text_2(text: str, justify: bool, max_chars_line: int = 40):
    curr_line = ''
    formatted_text = ''
    for token in text.split():
        aux_curr_line = f'{curr_line} {token}' if curr_line else token
        if len(aux_curr_line) <= 40:
            curr_line = aux_curr_line
            aux_curr_line = ''
        else:
            formatted_text = f'{formatted_text}\n{curr_line}' if formatted_text else curr_line
            curr_line = token
    if not aux_curr_line:
        formatted_text = f'{formatted_text}\n{curr_line}'
    if justify:
        formatted_text = justify_text(text=formatted_text, max_line_size=max_chars_line)
    return formatted_text


def _get_spaces_to_add(n_spaces_line: int, n_spaces_to_add: int):
    avg_spaces = int(n_spaces_to_add / n_spaces_line)

    spaces = list(range(n_spaces_line)) * avg_spaces

    remaining_spaces_to_add = n_spaces_to_add - len(spaces)

    spaces.extend([space for space in range(remaining_spaces_to_add)])

    return {space_index: spaces.count(space_index)
            for space_index in range(n_spaces_line)}


def _pad_line(line: str, n_spaces_to_add: int):
    tokens = line.split()

    n_spaces_line = len(tokens) - 1

    spaces_to_add = _get_spaces_to_add(n_spaces_line=n_spaces_line,
                                       n_spaces_to_add=n_spaces_to_add)

    padded_tokens = [f"{' ' * (num_spaces + 1)}{token}"
                     for token, num_spaces in zip(tokens[1:], spaces_to_add.values())]

    padded_line = f"{tokens[0]}{''.join(padded_tokens)}"

    return padded_line


def justify_text(text: str, max_line_size: int):
    justified_text_lines = []
    for line in text.splitlines():
        n_spaces_to_add = max_line_size - len(line)

        justified_text_lines.append(_pad_line(line, n_spaces_to_add)
                                    if n_spaces_to_add > 0
                                    else line)

    return '\n'.join(justified_text_lines)

if __name__ == "__main__":
    DEFAULT_TEXT = "In the beginning God created the heavens and the earth. " \
                   "Now the earth was formless and empty, darkness was over the surface of the deep, " \
                   "and the Spirit of God was hovering over the waters.\n \n" \
                   "And God said, \"Let there be light,\" and there was light. " \
                   "God saw that the light was good, and he separated the light from the darkness. " \
                   "God called the light \"day,\" and the darkness he called \"night.\" " \
                   "And there was evening, and there was morning - the first day."
    DEFAULT_LIMIT = 40
    DEFAULT_JUSTIFY = True
    print(format_text_2(text=DEFAULT_TEXT, justify=DEFAULT_JUSTIFY, max_chars_line=DEFAULT_LIMIT))