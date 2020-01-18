import re


def remove_parentheses(string):
    regex = r'\([^()]*\)'

    while True:
        string, replacements = re.subn(regex, '', string)
        if replacements == 0:
            break

    return string
