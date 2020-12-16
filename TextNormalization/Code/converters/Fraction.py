
from singleton_decorator import singleton

import re

from .Cardinal import Cardinal

@singleton
class Fraction:
    def __init__(self):
        super().__init__()
        self.filter_regex = re.compile(",")
        self.space_filter_regex = re.compile(" ")
        self.trans_dict = {
            "½": {
                "prepended": "a",
                "single": "one",
                "text": "half"
                },
            "⅓": {
                "prepended": "a",
                "single": "one",
                "text": "third"
                },
            "⅔": {
                "prepended": "two",
                "single": "two",
                "text": "thirds"
                },
            "¼": {
                "prepended": "a",
                "single": "one",
                "text": "quarter"
                },
            "¾": {
                "prepended": "three",
                "single": "three",
                "text": "quarters"
                },
            "⅕": {
                "prepended": "a",
                "single": "one",
                "text": "fifth"
                },
            "⅖": {
                "prepended": "two",
                "single": "two",
                "text": "fifths"
                },
            "⅗": {
                "prepended": "three",
                "single": "three",
                "text": "fifths"
                },
            "⅘": {
                "prepended": "four",
                "single": "four",
                "text": "fifths"
                },
            "⅙": {
                "prepended": "a",
                "single": "one",
                "text": "sixth"
                },
            "⅚": {
                "prepended": "five",
                "single": "five",
                "text": "sixths"
                },
            "⅐": {
                "prepended": "a",
                "single": "one",
                "text": "sixth"
                },
            "⅛": {
                "prepended": "an",
                "single": "one",
                "text": "eighth"
                },
            "⅜": {
                "prepended": "three",
                "single": "three",
                "text": "eighths"
                },
            "⅝": {
                "prepended": "five",
                "single": "five",
                "text": "eighths"
                },
            "⅞": {
                "prepended": "seven",
                "single": "seven",
                "text": "eighths"
                },
            "⅑": {
                "prepended": "a",
                "single": "one",
                "text": "ninth"
                },
            "⅒": {
                "prepended": "a",
                "single": "one",
                "text": "tenth"
                }
        }
        self.special_regex = re.compile(f"({'|'.join(self.trans_dict.keys())})")
        self.cardinal = Cardinal()

        self.slash_regex = re.compile(r"(-?\d{1,3}( \d{3})+|-?\d+) *\/ *(-?\d{1,3}( \d{3})+|-?\d+)")


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

        self.edge_dict = {
            "1": {
                "singular": "over one",
                "plural": "over one"
                },
            "2": {
                "singular": "half",
                "plural": "halves"
                },
            "4":{
                "singular": "quarter",
                "plural": "quarters"
                }
        }

    def convert(self, token: str) -> str:
        token = self.filter_regex.sub("", token)
        match = self.special_regex.search(token)
        if match:
            frac = match.group(1)
            frac_dict = self.trans_dict[frac]

            remainder = self.special_regex.sub("", token)
            if remainder:
                prefix = self.cardinal.convert(remainder)
                result = f"{prefix} and {frac_dict['prepended']} {frac_dict['text']}"
            else:
                result = f"{frac_dict['single']} {frac_dict['text']}"
        
        else:
            match = self.slash_regex.search(token)
            if match:
                numerator = match.group(1)
                denominator = match.group(3)

                numerator = self.space_filter_regex.sub("", numerator)
                denominator = self.space_filter_regex.sub("", denominator)

                numerator_text = self.cardinal.convert(numerator)


                if denominator in self.edge_dict:

                    result = f"{numerator_text} {self.edge_dict[denominator][('singular' if abs(int(numerator)) == 1 else 'plural')]}"
                
                else:

                    denominator_text_list = self.cardinal.convert(denominator).split(" ")
                    denominator_text_list[-1] = self.trans_denominator[denominator_text_list[-1]]

                    if abs(int(numerator)) != 1:
                        denominator_text_list[-1] += "s"
                    denominator_text = " ".join(denominator_text_list)
                    result = f"{numerator_text} {denominator_text}"
                

                remainder = self.slash_regex.sub("", token)
                if remainder:
                    remainder_text = self.cardinal.convert(remainder)

                    result_list = result.split()
                    if result_list[0] == "one":
                        result_list[0] = "a"

                    result = f"{remainder_text} and {' '.join(result_list)}"
            
            else:
                result = token

        return result
