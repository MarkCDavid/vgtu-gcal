from difflib import SequenceMatcher
from dateutil import parser as date_parser


def confirmation_prompt(prompt):
    return 'y' == input(f"{prompt} (y/n) ").lower()


def select_closest(select, collection, selector=lambda x: x):
    closest, ratio = None, 0
    for item in collection:
        new_ratio = SequenceMatcher(None, selector(item).lower(), select.lower()).ratio()
        if new_ratio >= ratio:
            closest, ratio = item, new_ratio
    return closest, ratio == 1


def select_closest_prompt(prompt, collection, default=lambda x: x[0], selector=lambda x: x):
    default = default(collection)
    while True:
        user_input = input(prompt if default is None else f"{prompt} (default '{selector(default)}') ")
        if len(user_input) == 0 and default is not None:
            return default
        closest, exact = select_closest(user_input, collection, selector)
        if exact or confirmation_prompt(f"Did you want to select '{selector(closest)}'? "):
            return closest


def date_prompt(default=''):
    while True:
        try:
            user_date = input(f"Date: (default '{default}') ")
            if len(user_date) == 0:
                return default
            date = date_parser.parse(user_date)
            return f"{date.year}-{date.month}-{date.day}"
        except ValueError:
            if not confirmation_prompt("Invalid date, try again?"):
                return default
