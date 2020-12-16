
from singleton_decorator import singleton

import re

from .Roman import Roman

@singleton
class Cardinal:
    def __init__(self):
        super().__init__()
        self.filter_regex = re.compile("[^0-9\-]")
        self.filter_strict_regex = re.compile("[^0-9]")
        self.dot_filter_regex = re.compile("[.]")

        # List of suffixes
        self.scale_suffixes = [
            "thousand", 
            "million", 
            "billion", 
            "trillion", 
            "quadrillion", 
            "quintillion", 
            "sextillion", 
            "septillion", 
            "octillion", 
            "undecillion", 
            "tredecillion", 
            "quattuordecillion", 
            "quindecillion", 
            "sexdecillion", 
            "septendecillion", 
            "octodecillion", 
            "novemdecillion", 
            "vigintillion"
        ]

        self.small_trans_dict = {
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

        self.tens_trans_dict = {
            "1": "ten",
            "2": "twenty",
            "3": "thirty",
            "4": "forty",
            "5": "fifty",
            "6": "sixty",
            "7": "seventy",
            "8": "eighty",
            "9": "ninety",
        }

        self.special_trans_dict = {
            11: "eleven",
            12: "twelve",
            13: "thirteen",
            14: "fourteen",
            15: "fifteen",
            16: "sixteen",
            17: "seventeen",
            18: "eighteen",
            19: "nineteen"
        }

        self.roman = Roman()

    def _give_chunk(self, num_str: str, size:int = 3) -> str:
        while num_str:
            yield num_str[-size:]
            num_str = num_str[:-size]

    def convert(self, token: str) -> str:
        token = self.dot_filter_regex.sub("", token)

        suffix = ""
        if self.roman.check_if_roman(token):
            token, suffix = self.roman.convert(token)

        token = self.filter_regex.sub("", token)

        prefix = ""
        while len(token) > 0 and token[0] == "-":
            token = token[1:]
            prefix = "minus" if prefix == "" else ""

        token = self.filter_strict_regex.sub("", token)

        text_list = []

        if token == len(token) * "0":
            text_list.append("zero")
        else:
            for depth, chunk in enumerate(self._give_chunk(token)):
                chunk_text_list = []
                hundred, rest = chunk[-3:-2], chunk[-2:]

                if len(hundred) != 0 and int(hundred) != 0:
                    chunk_text_list.append(self.small_trans_dict[hundred])
                    chunk_text_list.append("hundred")

                if int(rest) in self.special_trans_dict:
                    chunk_text_list.append(self.special_trans_dict[int(rest)])
                else:
                    if len(rest) == 2 and rest[-2] != "0":
                        chunk_text_list.append(self.tens_trans_dict[rest[-2]])
                    if rest[-1] != "0":
                        chunk_text_list.append(self.small_trans_dict[rest[-1]])

                if depth > 0 and len(chunk_text_list) > 0:
                    try:
                        chunk_text_list.append(self.scale_suffixes[depth-1])
                    except IndexError:
                        pass

                text_list = chunk_text_list + text_list

        token = " ".join(text_list)

        if prefix:
            token = f"{prefix} {token}"
        if suffix:
            token = f"{token}{suffix}"

        return token
