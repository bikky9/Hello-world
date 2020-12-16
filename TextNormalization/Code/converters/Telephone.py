
from singleton_decorator import singleton

import re

@singleton
class Telephone:
    def __init__(self):
        super().__init__()
        self.trans_dict = {
            " ": "sil",
            "-": "sil",

            "x": "extension",

            "0": "o",
            "1": "one",
            "2": "two",
            "3": "three",
            "4": "four",
            "5": "five",
            "6": "six",
            "7": "seven",
            "8": "eight",
            "9": "nine",
        }
        self.filter_regex = re.compile(r"[()]")

    def convert(self, token: str) -> str:
        token = self.filter_regex.sub("-", token.lower())

        result_list = [self.trans_dict[c] if c in self.trans_dict else c for c in token]

        result_list = [section for i, section in enumerate(result_list) if section != "sil" or (i - 1 >= 0 and result_list[i - 1] != "sil")]

        i = 0
        while i < len(result_list):
            offset = 0
            while i + offset < len(result_list) and result_list[i + offset] == "o":
                offset += 1

            if (i + offset >= len(result_list) or result_list[i + offset] == "sil") and (i - 1 < 0 or result_list[i - 1] not in ("o", "sil")) and offset in (2, 3):
                result_list[i : offset + i] = ["hundred"] if offset == 2 else ["thousand"]

            i += 1

        return " ".join(result_list)
