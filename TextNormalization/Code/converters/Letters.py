
from singleton_decorator import singleton

import re

from .Verbatim import Verbatim

@singleton
class Letters:
    def __init__(self):
        super().__init__()
        self.filter_regex = re.compile(r"[^A-Za-zÀ-ÖØ-öø-ÿ&']")
        self.first_word_regex = re.compile(r"")
        self.verbatim = Verbatim()
        self.trans_dict = {
            "é": "e acute",
        }
    
    def convert(self, token: str) -> str:

        if type(token) == float:
            return "n a"

        if " " in token and ". " not in token:
            token = token.split(" ")[0]

        if len(token) == 1:
            if token in self.trans_dict:
                return self.trans_dict[token]
            return token

        suffix = True

        if token[-1] == "-":
            suffix = False

        token = self.filter_regex.sub("", str(token))

        if suffix and len(token) >= 3 and token[-2:] in ("'s", "s'"):
            token = token[:-2]
        elif suffix and token and token[-1] == "s" and any([c.isupper() for c in token[:-1]]):
            token = token[:-1]
        else:
            suffix = False

        return " ".join([self.convert_char(char) for char in token if char != "'"]) + ("'s" if suffix else "")

    def convert_char(self, char: str) -> str:
        if char in self.trans_dict:
            return self.trans_dict[char]

        return self.verbatim.convert_char(char)
