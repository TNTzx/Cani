"""Contains the class for string variations."""

class StrVariations():
    """Defines variations of strings."""
    def __init__(self, string: str):
        self.original = string
        self.capitalize = string.capitalize()
        self.case_upper = string.upper()
        self.case_lower = string.lower()
        self.case_sentence = string.title()
