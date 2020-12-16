
from singleton_decorator import singleton

import re

from .Roman import Roman
from .Cardinal import Cardinal

@singleton
class Ordinal:
    def __init__(self):
        super().__init__()
        self.filter_regex = re.compile(r"[, ºª]")
        self.standard_case_regex = re.compile(r"(?i)(\d+)(th|nd|st|rd)(s?)")
        self.roman = Roman()
        self.cardinal = Cardinal()

        self.trans_denominator = {
            "zero": "zeroth",
            "one": "first",
            "two": "second",
            "three": "third",
            "four": "fourth",
            "five": "fifth",
            "six": "sixth",
            "seven": "seventh",
            "eight": "eighth",
            "nine": "ninth",

            "ten": "tenth",
            "twenty": "twentieth",
            "thirty": "thirtieth",
            "forty": "fortieth",
            "fifty": "fiftieth",
            "sixty": "sixtieth",
            "seventy": "seventieth",
            "eighty": "eightieth",
            "ninety": "ninetieth",

            "eleven": "eleventh",
            "twelve": "twelfth",
            "thirteen": "thirteenth",
            "fourteen": "fourteenth",
            "fifteen": "fifteenth",
            "sixteen": "sixteenth",
            "seventeen": "seventeenth",
            "eighteen": "eighteenth",
            "nineteen": "nineteenth",

            "hundred": "hundredth",
            "thousand": "thousandth",
            "million": "millionth",
            "billion": "billionth",
            "trillion": "trillionth",
            "quadrillion": "quadrillionth",
            "quintillion": "quintillionth",
            "sextillion": "sextillionth",
            "septillion": "septillionth",
            "octillion": "octillionth",
            "undecillion": "undecillionth",
            "tredecillion": "tredecillionth",
            "quattuordecillion": "quattuordecillionth",
            "quindecillion": "quindecillionth",
            "sexdecillion": "sexdecillionth",
            "septendecillion": "septendecillionth",
            "octodecillion": "octodecillionth",
            "novemdecillion": "novemdecillionth",
            "vigintillion": "vigintillionth"
        }
    
    def convert(self, token: str) -> str:

        token = self.filter_regex.sub("", token)

        prefix = ""
        suffix = ""
        if self.roman.check_if_roman(token):
            if not token.endswith(("th", "nd", "st", "rd")):
                prefix = "the"
            token, suffix = self.roman.convert(token)
        
        else:
            match = self.standard_case_regex.fullmatch(token)
            if match:
                token = match.group(1)
                suffix = match.group(3)

        number_text_list = self.cardinal.convert(token).split(" ")
        number_text_list[-1] = self.trans_denominator[number_text_list[-1]]
        result = " ".join(number_text_list)

        if prefix:
            result = f"{prefix} {result}"
        if suffix:
            result = f"{result}{suffix}"

        return result
