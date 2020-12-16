
from singleton_decorator import singleton

import re

@singleton
class Digit:
    def __init__(self):
        super().__init__()
        self.filter_regex = re.compile("[^0-9]")
        self.trans_dict = {
            "0": "o",
            "1": "one",
            "2": "two",
            "3": "three",
            "4": "four",
            "5": "five",
            "6": "six",
            "7": "seven",
            "8": "eight",
            "9": "nine"
        }

    def convert(self, token: str) -> str:
        token = self.filter_regex.sub("", token)
        if token == "007":
            return "double o seven"
        token = " ".join([self.trans_dict[c] for c in token])
        return token
