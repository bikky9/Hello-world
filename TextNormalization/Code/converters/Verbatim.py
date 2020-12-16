
from singleton_decorator import singleton

import re

@singleton
class Verbatim:
    def __init__(self):
        super().__init__()

        # Translation dict from some single characters to text
        self.trans_dict = {
            # Words
            "feet": "feet",

            # Characters
            "&": "and",
            "_": "underscore",
            "#": "number",
            "€": "euro",
            "$": "dollar",
            "£": "pound",
            "~": "tilde",
            "%": "percent",

            # Math related
            "²": "squared",
            "³": "cubed",
            "×": "times",
            "=": "equals",
            ">": "greater than",

            # Greek
            "α": "alpha",
            "Α": "alpha",
            "β": "beta",
            "Β": "beta",
            "γ": "gamma",
            "Γ": "gamma",
            "δ": "delta",
            "Δ": "delta",
            "ε": "epsilon",
            "Ε": "epsilon",
            "ζ": "zeta",
            "Ζ": "zeta",
            "η": "eta",
            "Η": "eta",
            "θ": "theta",
            "Θ": "theta",
            "ι": "iota",
            "Ι": "iota",
            "κ": "kappa",
            "Κ": "kappa",
            "λ": "lambda",
            "Λ": "lambda",
            "Μ": "mu",
            "μ": "mu",
            "ν": "nu",
            "Ν": "nu",
            "ξ": "xi",
            "Ξ": "xi",
            "ο": "omicron",
            "Ο": "omicron",
            "π": "pi",
            "Π": "pi",
            "ρ": "rho",
            "Ρ": "rho",
            "ς": "sigma",
            "σ": "sigma",
            "Σ": "sigma",
            "Ϲ": "sigma",
            "ϲ": "sigma",
            "τ": "tau",
            "Τ": "tau",
            "υ": "upsilon",
            "Υ": "upsilon",
            "φ": "phi",
            "Φ": "phi",
            "χ": "chi",
            "Χ": "chi",
            "ψ": "psi",
            "Ψ": "psi",
            "ω": "omega",
            "Ω": "omega",
            "µ": "micro"
        }

        self.trans_ordinal_dict = {
            ".": "dot",
            "-": "d a s h",

            "0": "o",
            "1": "o n e",
            "2": "t w o",
            "3": "t h r e e",
            "4": "f o u r",
            "5": "f i v e",
            "6": "s i x",
            "7": "s e v e n",
            "8": "e i g h t",
            "9": "n i n e"
        }

    def convert(self, token: str) -> str:
        if token in self.trans_dict:
            return self.trans_dict[token]

        if len(token) == 1:
            return token

        return " ".join([self.convert_char(c) for c in token])

    def convert_char(self, char: str) -> str:
        if char in self.trans_ordinal_dict:
            return self.trans_ordinal_dict[char]

        if char in self.trans_dict:
            return self.trans_dict[char]

        return char.lower()
