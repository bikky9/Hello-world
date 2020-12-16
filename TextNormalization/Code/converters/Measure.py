
from singleton_decorator import singleton

import re

from .Decimal import Decimal
from .Fraction import Fraction

@singleton
class Measure:
    def __init__(self):
        super().__init__()
        self.fraction_regex = re.compile(r"(((?:-?\d* )?-?\d+ *\/ *-? *\d+)|(-?\d* *(?:½|⅓|⅔|¼|¾|⅕|⅖|⅗|⅘|⅙|⅚|⅐|⅛|⅜|⅝|⅞|⅑|⅒)))")
        self.of_a_regex = re.compile(r"(-?\d+ -?\d+ *\/ *-? *\d+)|(-?\d+ *(?:½|⅓|⅔|¼|¾|⅕|⅖|⅗|⅘|⅙|⅚|⅐|⅛|⅜|⅝|⅞|⅑|⅒))")
        self.value_regex = re.compile(r"(-?(?: |\d)*\.?\d+ *(?:thousand|million|billion|trillion|quadrillion|quintillion|sextillion|septillion|octillion|undecillion|tredecillion|quattuordecillion|quindecillion|sexdecillion|septendecillion|octodecillion|novemdecillion|vigintillion)?)")
        self.filter_regex = re.compile(r"[,]")
        self.filter_space_regex = re.compile(r"[ ]")
        self.letter_filter_regex = re.compile(r"[^0-9\-\.]")

        self.prefix_dict = {
            "Y": "yotta",
            "Z": "zetta",
            "E": "exa",
            "P": "peta",
            "T": "tera",
            "G": "giga",
            "M": "mega",
            "k": "kilo",
            "h": "hecto",
            "da": "deca",
            "d": "deci",
            "c": "centi",
            "m": "milli",
            "μ": "micro",
            "µ": "micro", # legacy symbol. 
            "n": "nano",
            "p": "pico",
            "f": "femto",
            "a": "atto",
            "z": "zepto",
            "y": "yocto"
        }

        self.prefixable_trans_dict = {
            "m": {
                "singular": "meter",
                "plural": "meters"
            },
            "b": {
                "singular": "bit", # Note that this messes with byte whenever the lowercase is used
                "plural": "bits"
            },
            "B": {
                "singular": "byte",
                "plural": "bytes"
            },
            "bps": {
                "singular": "bit per second", # Note that this messes with byte whenever the lowercase is used
                "plural": "bits per second"
            },
            "Bps": {
                "singular": "byte per second",
                "plural": "bytes per second"
            },
            "g": {
                "singular": "gram",
                "plural": "grams"
            },
            "gf": {
                "singular": "gram force",
                "plural": "grams force"
            },
            "W": {
                "singular": "watt",
                "plural": "watts"
            },
            "Wh": {
                "singular": "watt hour",
                "plural": "watt hours"
            },
            "Hz": {
                "singular": "hertz",
                "plural": "hertz"
            },
            "hz": {
                "singular": "hertz",
                "plural": "hertz"
            },
            "J": {
                "singular": "joule",
                "plural": "joules"
            },
            "L": {
                "singular": "liter",
                "plural": "liters"
            },
            "V": {
                "singular": "volt",
                "plural": "volts"
            },
            "f": {
                "singular": "farad",
                "plural": "farads"
            },
            "s": {
                "singular": "second",
                "plural": "seconds"
            },
            "A": {
                "singular": "ampere",
                "plural": "amperes"
            },
            "Ah": {
                "singular": "amp hour",
                "plural": "amp hours"
            },
            "Pa": {
                "singular": "pascal",
                "plural": "pascals"
            },
            "s": {
                "singular": "second",
                "plural": "seconds"
            },
            "C": {
                "singular": "coulomb",
                "plural": "coulombs"
            },
            "Bq": {
                "singular": "becquerel",
                "plural": "becquerels"
            },
            "N": {
                "singular": "newton",
                "plural": "newtons"
            },
            "bar": {
                "singular": "bar",
                "plural": "bars"
            },
            "lm": { # TODO: This turns "Klm" -> "kilolumens", while Kilometer may have been intended?
                "singular": "lumen",
                "plural": "lumens"
            },
            "cal": {
                "singular": "calorie",
                "plural": "calories"
            },
        }

        self.prefixed_dict = {prefix + prefixed: {"singular": self.prefix_dict[prefix] + self.prefixable_trans_dict[prefixed]["singular"], "plural": self.prefix_dict[prefix] + self.prefixable_trans_dict[prefixed]["plural"]} for prefixed in self.prefixable_trans_dict for prefix in self.prefix_dict}
        self.prefixed_dict = {**self.prefixed_dict, **self.prefixable_trans_dict}

        self.custom_dict = {
            "%": {
                "singular": "percent",
                "plural": "percent"
            },
            "pc": {
                "singular": "percent",
                "plural": "percent"
            },
            "ft": {
                "singular": "foot",
                "plural": "feet"
            },
            "mi": {
                "singular": "mile",
                "plural": "miles"
            },
            "mb": {
                "singular": "megabyte",
                "plural": "megabytes"
            },
            "ha": {
                "singular": "hectare",
                "plural": "hectares"
            },
            "\"": {
                "singular": "inch",
                "plural": "inches"
            },
            "in": {
                "singular": "inch",
                "plural": "inches"
            },
            "\'": {
                "singular": "foot",
                "plural": "feet"
            },
            "rpm": {
                "singular": "revolution per minute",
                "plural": "revolutions per minute" # on "per x", x is always singular
            },
            "hp": {
                "singular": "horsepower",
                "plural": "horsepower"
            },
            "cc": {
                "singular": "c c",
                "plural": "c c"
            },
            "oz": {
                "singular": "ounce",
                "plural": "ounces",
            },
            "mph": {
                "singular": "mile per hour",
                "plural": "miles per hour"
            },
            "lb": {
                "singular": "pound",
                "plural": "pounds"
            },
            "lbs": {
                "singular": "pounds", # Always plural due to how "lbs" itself is already plural
                "plural": "pounds"
            },
            "kt": {
                "singular": "knot",
                "plural": "knots"
            },
            "dB": {
                "singular": "decibel",
                "plural": "decibels"
            },
            "AU": {
                "singular": "astronomical unit",
                "plural": "astronomical units"
            },
            "st": {
                "singular": "stone",
                "plural": "stone" # Stone is always singular, eg "nine stone"
            },
            "yd": {
                "singular": "yard",
                "plural": "yards"
            },
            "yr": {
                "singular": "year",
                "plural": "years"
            },
            "yrs": {
                "singular": "year", #TODO Consider years as "yrs" is already plural
                "plural": "years"
            },
            "eV": {
                "singular": "electron volt",
                "plural": "electron volts"
            },
            "/": {
                "singular": "per",
                "plural": "per"
            },
            "sq": {
                "singular": "square",
                "plural": "square"
            },
            "2": {
                "singular": "square",
                "plural": "square"
            },
            "²": {
                "singular": "square",
                "plural": "square"
            },
            "3": {
                "singular": "cubic",
                "plural": "cubic"
            },
            "³": {
                "singular": "cubic",
                "plural": "cubic"
            },
            "h": {
                "singular": "hour",
                "plural": "hours"
            },
            "hr": {
                "singular": "hour",
                "plural": "hours"
            },
            "hrs": {
                "singular": "hour", # TODO: Consider plural as "hrs" is already plural
                "plural": "hours"
            },
            "ch": {
                "singular": "chain",
                "plural": "chains"
            },
            "KiB": {
                "singular": "kibibyte",
                "plural": "kibibytes"
            },
            "MiB": {
                "singular": "mebibyte",
                "plural": "mebibytes"
            },
            "GiB": {
                "singular": "gibibyte",
                "plural": "gibibytes"
            },
            "pH": { # The data parses "pH" as "pico henrys"
                "singular": "p h",
                "plural": "p h"
            },
            "kph": {
                "singular": "kilometer per hour",
                "plural": "kilometers per hour"
            },
            "Da": {
                "singular": "dalton",
                "plural": "daltons"
            },
            "cwt": {
                "singular": "hundredweight",
                "plural": "hundredweight"
            },
            "Sv": {
                "singular": "sievert",
                "plural": "sieverts",
            },
            "C": { # Overrides Coulomb
                "singular": "celcius", 
                "plural": "celcius"
            },
            "degrees": {
                "singular": "degree",
                "plural": "degrees"
            },
            "degree": {
                "singular": "degree",
                "plural": "degrees"
            },
            "atm": {
                "singular": "atmosphere",
                "plural": "atmospheres"
            },
            "min": {
                "singular": "minute",
                "plural": "minutes"
            },
            "cd": {
                "singular": "candela",
                "plural": "candelas"
            },
            "ly": {
                "singular": "light year",
                "plural": "light years"
            },
            "kts": {
                "singular": "knot",
                "plural": "knots"
            },
            "mol": {
                "singular": "mole",
                "plural": "moles"
            },
            "Nm": { # Overrides nanometers on the lowercase
                "singular": "newton meter",
                "plural": "newton meters"
            },
            "Ω": {
                "singular": "ohm",
                "plural": "ohms"
            },
            "bbl": {
                "singular": "barrel",
                "plural": "barrels"
            },
            "gal": {
                "singular": "gallon",
                "plural": "gallons"
            },
            "cal": { # This overides "cal" from calorie, while preserving eg "kcal". "cal" is more often used to refer to caliber than calorie I reckon, hence this entry
                "singular": "cal",
                "plural": "cal"
            }
        }

        self.prefixed_dict = {**self.prefixed_dict, **self.custom_dict}

        self.lower_prefixed_dict = {key.lower(): self.prefixed_dict[key] for key in self.prefixed_dict}
        self.special_suffixes = re.compile(r"(\/|per(?!cent)|sq|2|²|3|³)")

        self.decimal = Decimal()
        self.fraction = Fraction()

    def convert(self, token: str) -> str:
        token = self.filter_regex.sub("", token)
        
        result_list = []

        plural = False

        match = self.fraction_regex.match(token)
        if match:
            result_list.append(self.fraction.convert(match.group(0)))
            token = token[:match.span()[0]] + token[match.span()[1]:]

            token = self.filter_space_regex.sub("", token)

            if self.of_a_regex.match(match.group(0)):
                plural = True
            else:
                result_list.append("of an" if token and token[0] in list("aeiou") else "of a")
            
        else:
            match = self.value_regex.match(token)
            if match:
                result_list.append(self.decimal.convert(self.filter_space_regex.sub("", match.group(1))))
                token = token[:match.span()[0]] + token[match.span()[1]:]
                if abs(float(self.letter_filter_regex.sub("", match.group(1)))) != 1 or "." in match.group(1):
                    plural = True

        per = False
        for split_token in token.split(" "):
            for i, token in enumerate(self.split_token(split_token)):
                if token in self.prefixed_dict:
                    result_list.append(self.prefixed_dict[token]["plural" if plural and not per else "singular"])
                elif token.lower() in self.lower_prefixed_dict:
                    result_list.append(self.lower_prefixed_dict[token.lower()]["plural" if plural and not per else "singular"])
                else:
                    result_list.append(token)

                if result_list[-1] == "per" and i != 0:
                    per = True

                elif result_list[-1] not in ("square", "cubic"):
                    per = False
        
        result = " ".join(result_list)

        result = re.sub(r"cubic centimeters?", "c c", result)

        return result
    
    def split_token(self, token: str) -> str:
        while True:
            match = self.special_suffixes.search(token)
            if match:
                s1, s2 = match.span()
                if match.group(1) in ("sq", "2", "²", "3", "³"):
                    yield token[s1:s2]
                    if token[:s1]:
                        yield token[:s1]
                else:
                    if token[:s1]:
                        yield token[:s1]
                    yield token[s1:s2]

                token = token[s2:]
            else:
                if token:
                    yield token
                break
