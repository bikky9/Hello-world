
from singleton_decorator import singleton

import re, os

from .Cardinal import Cardinal
from .Digit import Digit

@singleton
class Money:
    def __init__(self):
        super().__init__()
        self.decimal_regex = re.compile(r"(.*?)(-?\d*)\.(\d+)(.*)")
        self.number_regex = re.compile(r"(.*?)(-?\d+)(.*)")
        self.filter_regex = re.compile(r"[, ]")
        self.currencies = {
            "$": {
                "number":{
                    "singular": "dollar",
                    "plural":   "dollars"
                },
                "decimal":{
                    "singular": "cent",
                    "plural":   "cents"
                }
            },
            "usd": {
                "number":{
                    "singular": "united states dollar",
                    "plural":   "united states dollars"
                },
                "decimal":{
                    "singular": "cent",
                    "plural":   "cents"
                }
            },
            "€": {
                "number":{
                    "singular": "euro",
                    "plural":   "euros"
                },
                "decimal":{
                    "singular": "cent",
                    "plural":   "cents"
                }
            },
            "£": {
                "number":{
                    "singular": "pound",
                    "plural":   "pounds"
                },
                "decimal":{
                    "singular": "penny",
                    "plural":   "pence"
                }
            }
        }
        with open(os.path.join(os.path.dirname(__file__), "money.json"), "r") as f:
            import json
            self.currencies = {**json.load(f), **self.currencies}
        self.suffixes = [
            "lakh",
            "crore",
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
        self.abbr_suffixes = {
            "k": "thousand",
            "m": "million",
            "bn": "billion",
            "b": "billion",
            "t": "trillion",
            
            "cr": "crore",
            "crores": "crore",
            "lakhs": "lakh",
            "lacs": "lakh"
        }

        #self.suffix_regex = re.compile(f"({'|'.join( sorted(self.suffixes + list(self.abbr_suffixes.keys()), key=len, reverse=True) )})(.*)", flags=re.I)
        self.suffix_regex = re.compile(f"(quattuordecillion|septendecillion|novemdecillion|quindecillion|octodecillion|tredecillion|sexdecillion|vigintillion|quadrillion|quintillion|undecillion|sextillion|septillion|octillion|thousand|trillion|million|billion|crores|crore|lakhs|lakh|lacs|bn|cr|k|m|b|t)(.*)", flags=re.I)

        #self.suffix_regex = re.compile(r"(quattuordecillion|septendecillion|novemdecillion|quindecillion|octodecillion|tredecillion|sexdecillion|vigintillion|quadrillion|quintillion|undecillion|sextillion|septillion|octillion|thousand|trillion|million|billion|crores|crore|lakhs|lakh|lacs|bn|cr|k|m|b|t)")
        self.currency_regex = re.compile(r"(.*?)(dollar|usd|rs\.|r\$|aed|afn|all|amd|ang|aoa|ars|aud|awg|azn|bam|bbd|bdt|bgn|bhd|bif|bmd|bnd|bob|brl|bsd|btc|btn|bwp|byn|bzd|cad|cdf|chf|clf|clp|cnh|cny|cop|crc|cuc|cup|cve|czk|djf|dkk|dop|dzd|egp|ern|etb|eur|fjd|fkp|gbp|gel|ggp|ghs|gip|gmd|gnf|gtq|gyd|hkd|hnl|hrk|htg|huf|idr|ils|imp|inr|iqd|irr|isk|jep|jmd|jod|jpy|kes|kgs|khr|kmf|kpw|krw|kwd|kyd|kzt|lak|lbp|lkr|lrd|lsl|lyd|mad|mdl|mga|mkd|mmk|mnt|mop|mro|mru|mur|mvr|mwk|mxn|myr|mzn|nad|ngn|nio|nok|npr|nzd|omr|pab|pen|pgk|php|pkr|pln|pyg|qar|ron|rsd|rub|rwf|sar|sbd|scr|sdg|sek|sgd|shp|sll|sos|srd|ssp|std|stn|svc|syp|szl|thb|tjs|tmt|tnd|top|try|ttd|twd|tzs|uah|ugx|usd|uyu|uzs|vef|vnd|vuv|wst|xaf|xag|xau|xcd|xdr|xof|xpd|xpf|xpt|yer|zar|zmw|zwl|fim|bef|cyp|ats|ltl|zl|u\$s|rs|tk|r$|dm|\$|€|£|¥)(.*?)", flags=re.I)

        self.cardinal = Cardinal()
        self.digit = Digit()

    def convert(self, token: str) -> str:

        token = self.filter_regex.sub("", token)

        before = ""
        after = ""

        currency = None

        number = ""
        decimal = ""

        scale = ""

        match = self.decimal_regex.search(token[::-1])
        if match:
            before = match.group(4)[::-1]
            number = match.group(3)[::-1]
            decimal = match.group(2)[::-1]
            after = match.group(1)[::-1]
        
        else:
            match = self.number_regex.search(token)
            if match:
                before = match.group(1)
                number = match.group(2)
                after = match.group(3)
        

        if before:
            before = before.lower()
            if before in self.currencies:
                currency = self.currencies[before]
            elif before[-1] in self.currencies:
                currency = self.currencies[before[-1]]


        if after:
            match = self.suffix_regex.match(after)
            if match:
                scale = match.group(1).lower()
                scale = self.abbr_suffixes[scale] if scale in self.abbr_suffixes else scale
                after = match.group(2)

            if after.lower() in self.currencies:
                currency = self.currencies[after.lower()]
                after = ""

        decimal_support = currency and "number" in currency

        result_list = []
        if decimal_support and not scale:
            if number and (number != "0" or not decimal):
                result_list.append(self.cardinal.convert(number))
                result_list.append(currency["number"]["singular" if number == "1" else "plural"])
                if decimal and decimal != "0" * len(decimal):
                    result_list.append("and")
            if decimal and decimal != "0" * len(decimal):
                decimal = f"{decimal:0<2}"
                result_list.append(self.cardinal.convert(decimal))
                result_list.append(currency["decimal"]["singular" if decimal == "01" else "plural"])
        
        else:
            if number:
                result_list.append(self.cardinal.convert(number))
            if decimal and decimal != "0" * len(decimal):
                result_list.append("point")
                result_list.append(self.digit.convert(decimal))
            if scale:
                result_list.append(scale)
            if currency:
                if decimal_support:
                    currency = currency["number"]
                if number == "1" and not decimal and not scale:
                    result_list.append(currency["singular"])
                else:
                    result_list.append(currency["plural"])

        if after:
            result_list.append(after.lower())

        result = " ".join(result_list)

        return result
