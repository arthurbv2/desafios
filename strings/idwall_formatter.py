def format_text(text: str, justify: bool, max_chars_line: int = 40):
    """
    format a text to have a given maximum number of characters by line
    :param text: a text
    :param justify: a boolean that'll check if a given text should or not be justified
    :param max_chars_line: the maximum number of characters by line
    :return: the formatted text with the given maximum number of characters by line
    """
    paragraphs = []
    for paragraph in text.splitlines():
        if paragraph.strip():
            curr_line = ''
            formatted_paragraph = ''
            for token in paragraph.split():
                aux_curr_line = f'{curr_line} {token}' if curr_line else token
                if len(aux_curr_line) <= 40:
                    curr_line = aux_curr_line
                    aux_curr_line = ''
                else:
                    formatted_paragraph = f'{formatted_paragraph}\n{curr_line}' if formatted_paragraph else curr_line
                    curr_line = token
            if not aux_curr_line:
                formatted_paragraph = f'{formatted_paragraph}\n{curr_line}'
            if justify:
                formatted_paragraph = _justify_text(text=formatted_paragraph, max_line_size=max_chars_line)
            paragraphs.append(formatted_paragraph)
        else:
            paragraphs.append('\n')
    return '\n'.join(paragraphs)


def _get_spaces_to_add(n_spaces_line: int, n_spaces_to_add: int):
    """
    This function gets the number of spaces in a line and
    the number of spaces that must be added in that line to
    distribute these spaces in the already existent ones
    :param n_spaces_line: number of spaces in the line
    :param n_spaces_to_add: number of spaces that needs to be added
    :return: a dict with the number of spaces that will be added at each indexed space
    """
    avg_spaces = int(n_spaces_to_add / n_spaces_line)

    spaces = list(range(n_spaces_line)) * avg_spaces

    remaining_spaces_to_add = n_spaces_to_add - len(spaces)

    spaces.extend([space for space in range(remaining_spaces_to_add)])

    return {space_index: spaces.count(space_index)
            for space_index in range(n_spaces_line)}


def _pad_line(line: str, n_spaces_to_add: int):
    """
    This function will pad a text line, which means that
    it'll add spaces in the existent ones in a manner that
    it reaches a given maximum number of characters in a line
    :param line: the text line
    :param n_spaces_to_add: the number of spaces that must to be added
    :return: a padded line string
    """
    tokens = line.split()

    n_spaces_line = len(tokens) - 1

    spaces_to_add = _get_spaces_to_add(n_spaces_line=n_spaces_line,
                                       n_spaces_to_add=n_spaces_to_add)

    padded_tokens = [f"{' ' * (num_spaces + 1)}{token}"
                     for token, num_spaces in zip(tokens[1:], spaces_to_add.values())]

    padded_line = f"{tokens[0]}{''.join(padded_tokens)}"

    return padded_line


def _justify_text(text: str, max_line_size: int):
    """
    This function justifies a text with respect to
    some maximum number of character per line
    :param text: a text
    :param max_line_size: the maximum number of character per line
    :return: a justified text
    """
    justified_text_lines = []
    for line in text.splitlines():
        n_spaces_to_add = max_line_size - len(line)

        justified_text_lines.append(_pad_line(line, n_spaces_to_add)
                                    if n_spaces_to_add > 0
                                    else line)

    return '\n'.join(justified_text_lines)
