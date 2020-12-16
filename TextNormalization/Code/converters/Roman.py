
from singleton_decorator import singleton

import re

@singleton
class Roman:
    def __init__(self):
        super().__init__()
        self.roman_filter_strict_regex = re.compile("[^IVXLCDM]")
        self.roman_filter_regex = re.compile(r"[.IVXLCDM]+(th|nd|st|rd|'s|s)?")

        self.roman_numerals = {
            "I": 1,
            "V": 5,
            "X": 10,
            "L": 50,
            "C": 100,
            "D": 500,
            "M": 1000
        }

    def convert(self, token: str) -> (str, str):
        token = max(token.split(" "), key=len)

        suffix = ""
        if token[-1:] == "s":
            suffix = "'s"

        token = self.roman_filter_strict_regex.sub("", token)

        total = 0
        prev = 0
        for c in reversed(token):
            cur = self.roman_numerals[c]
            total += cur if cur >= prev else -cur
            prev = cur

        return (str(total), suffix)
    
    def check_if_roman(self, token: str) -> bool:
        return self.roman_filter_regex.fullmatch(max(token.split(" "), key=len)) != None
