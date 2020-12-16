
from singleton_decorator import singleton

import re

from .Cardinal import Cardinal
from .Digit import Digit

@singleton
class Electronic:
    def __init__(self):
        super().__init__()
        self.data_https_dict = {
            "/": "slash",
            ":": "colon",
            ".": "dot",
            "#": "hash",
            "-": "dash",

            "é": "e a c u t e",

            "(": "o p e n i n g p a r e n t h e s i s",
            ")": "c l o s i n g p a r e n t h e s i s",
            "_": "u n d e r s c o r e",
            ",": "c o m m a",
            "%": "p e r c e n t",
            "~": "t i l d e",
            ";": "s e m i colon",
            "'": "s i n g l e q u o t e",
            "\"": "d o u b l e q u o t e",

            "0": "o",
            "1": "o n e",
            "2": "t w o",
            "3": "t h r e e",
            "4": "f o u r",
            "5": "f i v e",
            "6": "s i x",
            "7": "s e v e n",
            "8": "e i g h t",
            "9": "n i n e",
        }
        self.data_no_https_dict = {
            "/": "s l a s h",
            ":": "c o l o n",
            ".": "dot",
            "#": "h a s h",
            "-": "d a s h",

            "é": "e a c u t e",
            
            "(": "o p e n i n g p a r e n t h e s i s",
            ")": "c l o s i n g p a r e n t h e s i s",
            "_": "u n d e r s c o r e",
            ",": "c o m m a",
            "%": "p e r c e n t",
            "~": "t i l d e",
            ";": "s e m i c o l o n",
            "'": "s i n g l e q u o t e",
            "\"": "d o u b l e q u o t e",
            
            "0": "o",
            "1": "o n e",
            "2": "t w o",
            "3": "t h r e e",
            "4": "f o u r",
            "5": "f i v e",
            "6": "s i x",
            "7": "s e v e n",
            "8": "e i g h t",
            "9": "n i n e",
        }

        self.data_http_regex = re.compile(r"https?://")

        self.sensible_trans_dict = {
            "/": "slash",
            ":": "colon",
            ".": "dot",
            "#": "hash",
            "-": "dash",
            "é": "e acute",
            "(": "opening parenthesis",
            ")": "closing parenthesis",
            "_": "underscore",
            ",": "comma",
            "%": "percent",
            "~": "tilde",
            ";": "semicolon",
            "'": "single quote",
            "\"": "double quote",

            "0": "zero",
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

        self.cardinal = Cardinal()
        self.digit = Digit()

    def convert(self, token: str) -> str:
        token = token.lower()

        if token == "::":
            return token

        if token[0] == "#" and len(token) > 1:
            return self.convert_hash_tag(token)

        http = self.data_http_regex.match(token) != None

        data_trans_dict = self.data_https_dict if http else self.data_no_https_dict
        
        result_list = []
        c_index = 0
        while c_index < len(token):
            if http:

                if token[c_index:].startswith(".com"):
                    result_list.append("dot com")
                    c_index += len(".com")
                    continue
            

            offset = 0
            while c_index + offset < len(token) and token[c_index + offset].isdigit():
                offset += 1

            if offset == 2 and token[c_index] != "0":
                text = self.cardinal.convert(token[c_index:c_index + offset])
                result_list.append(" ".join([c for c in text if c != " "]))
                c_index += offset
            elif offset > 0 and token[c_index] != "0" * offset:
                text = self.digit.convert(token[c_index:c_index + offset])
                result_list.append(" ".join([c for c in text if c != " "]))
                c_index += offset
            else:

                if token[c_index] in data_trans_dict:
                    result_list.append(data_trans_dict[token[c_index]])
                else:
                    result_list.append(token[c_index])                    
                c_index += 1

        return " ".join(result_list)

    def sensible_convert(self, token: str) -> str:
        token = token.lower()

        if token == "::":
            return token

        if token[0] == "#" and len(token) > 1:
            return self.convert_hash_tag(token)

        result_list = []
        c_index = 0
        while c_index < len(token):
            if token[c_index:].startswith(".com"):
                result_list.append("dot com")
                c_index += 4
                continue

            char = token[c_index]
            if char in self.sensible_trans_dict:
                result_list.append(self.sensible_trans_dict[char])
            else:
                result_list.append(char)

            c_index += 1
        
        return " ".join(result_list)
    
    def convert_hash_tag(self, token: str) -> str:
        out = "hash tag "
        for char in token[1:].lower():
            if char in self.sensible_trans_dict:
                if out[-1] == " ":
                    out += self.sensible_trans_dict[char] + " "
                else:
                    out += " " + self.sensible_trans_dict[char] + " "
            else:
                out += char
        return out.strip()
