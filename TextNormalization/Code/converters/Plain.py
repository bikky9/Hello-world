
from singleton_decorator import singleton

import re, os

@singleton
class Plain:
    def __init__(self):
        super().__init__()
        self.upper_trans_dict = {
            "DR": "drive", # Also often "Doctor"
            "ST": "street"
        }
        self.trans_dict = {
        }

        with open(os.path.join(os.path.dirname(__file__), "plain.json")) as f:
            import json
            self.trans_dict = {**self.trans_dict, **json.load(f)}

        self.split_at = [
            "strasse",
            "weg",
        ]

        self.split_at_regex = re.compile(f"(.*)({'|'.join(self.split_at)})$", flags=re.I)
    
    def convert(self, token: str) -> str:
        if isinstance(token, float):
            return "NaN"

        if token in self.upper_trans_dict:
            return self.upper_trans_dict[token]

        if token.lower() in self.trans_dict:
            return self.trans_dict[token.lower()]

        token = re.sub(r"[^a-zA-ZÀ-ÖØ-öø-ÿ0-9']", "", token)

        if token.lower().endswith(tuple(self.split_at)):
            groups = self.split_at_regex.match(token).groups()
            if groups[0]:
                token = " ".join(groups).lower()

        return token
