
from singleton_decorator import singleton

import re

from .Cardinal import Cardinal
from .Digit import Digit

@singleton
class Address:
    def __init__(self):
        super().__init__()
        self.filter_regex = re.compile(r"[. -]")
        self.address_regex = re.compile(r"((?P<upper_prefix>[A-Z\.]*)|(?P<lower_prefix>[a-zA-Z]*))(?P<link>( |-)*)(?P<number>\d+)(?P<suffix>N|E|S|W|n|e|s|w)?")
        self.direction_trans_dict = {
            "n": "north",
            "e": "east",
            "s": "south",
            "w": "west",
        }
        self.cardinal = Cardinal()
        self.digit = Digit()

    def convert(self, token: str) -> str:

        token = token.strip()
        
        result_list = []
        match = self.address_regex.match(token)
        if match:
            lower_prefix, upper_prefix, link, number, suffix = match.group("lower_prefix"), match.group("upper_prefix"), match.group("link"), match.group("number"), match.group("suffix")
            if lower_prefix:
                result_list.append(lower_prefix.lower())
            elif upper_prefix:
                result_list += [c for c in upper_prefix.lower() if c != "."]
            if ((link or number[-1] == "0" or number[0] == "0") and len(number) == 3) or len(number) == 2:
                if number[-3:-2]:
                    result_list.append(self.digit.convert(number[-3:-2]))
                if number[-2:-1] == "0":
                    result_list.append("o")
                    result_list.append(self.digit.convert(number[-1]))
                else:
                    result_list.append(self.cardinal.convert(number[-2:]))
            else:
                result_list.append(self.digit.convert(number))
            if suffix:
                result_list.append(self.direction_trans_dict[suffix.lower()])

            return " ".join(result_list)
        
        return token
