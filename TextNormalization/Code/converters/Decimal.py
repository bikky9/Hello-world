
from singleton_decorator import singleton

import re

from .Digit import Digit
from .Cardinal import Cardinal

@singleton
class Decimal:
    def __init__(self):
        super().__init__()
        self.decimal_regex = re.compile(r"(-?\d*)\.(\d+)(.*)")
        self.number_regex = re.compile(r"(-?\d+)(.*)")
        self.filter_regex = re.compile(r"[,]")
        self.cardinal = Cardinal()
        self.digit = Digit()
        self.suffixes = [
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
        self.suffix_regex = re.compile(f" *({'|'.join(self.suffixes)})")
        self.e_suffix_regex = re.compile(r" *E(-?\d+)")
    
    def convert(self, token: str) -> str:

        token = self.filter_regex.sub("", token)

        number = ""
        decimal = ""

        match = self.decimal_regex.match(token)
        if match:
            number = match.group(1)
            decimal = match.group(2)
            token = match.group(3)

        else:
            match = self.number_regex.match(token)
            if match:
                number = match.group(1)
                token = match.group(2)

        match = self.suffix_regex.match(token)
        suffix = ""
        if match:
            suffix = match.group(1)
        else:
            match = self.e_suffix_regex.match(token)
            if match:
                suffix = f"times ten to the {self.cardinal.convert(match.group(1))}"

        result_list = []
        if len(decimal) > 0:
            result_list.append("point")
            if decimal == "0" and len(number) > 0 and len(suffix) == 0:
                result_list.append("zero")
            else:
                result_list.append(self.digit.convert(decimal))

        if number:
            result_list.insert(0, self.cardinal.convert(number))

        if suffix:
            result_list.append(suffix)

        result = " ".join(result_list)
        
        return result
