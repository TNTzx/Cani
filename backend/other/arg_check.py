"""Contains logic for checking arguments passed to a function."""


def choice_check(parameter, choices: list):
    """Raises `ValueError` if `parameter` is not in `choices`."""
    if parameter not in choices:
        raise ValueError(f"Argument {parameter} not in {choices}.")
