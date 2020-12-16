
from singleton_decorator import singleton

import re

from .Cardinal import Cardinal
from .Ordinal import Ordinal

@singleton
class Date:
    def __init__(self):
        super().__init__()
        self.filter_regex = re.compile(r"[,']")

        self.day_regex = re.compile(r"^(?P<prefix>monday|tuesday|wednesday|thursday|friday|saturday|sunday|mon|tue|wed|thu|fri|sat|sun)\.?", flags=re.I)

        self.dash_date_ymd_regex = re.compile(r"^(?P<year>\d{2,5}) *(?:-|\.|/) *(?P<month>\d{1,2}) *(?:-|\.|/) *(?P<day>\d{1,2})$", flags=re.I)

        self.dash_date_mdy_regex = re.compile(r"^(?P<month>\d{1,2}) *(?:-|\.|/) *(?P<day>\d{1,2}) *(?:-|\.|/) *(?P<year>\d{2,5})$", flags=re.I)


        self.text_ymd_regex = re.compile(r"^(?P<year>\d{2,5}) *(?:-|\.|/) *(?P<month>january|february|march|april|may|june|july|august|september|october|november|december|sept|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec) *(?:-|\.|/) *(?P<day>\d{1,2})$", flags=re.I)

        self.text_dmy_regex = re.compile(r"^(?P<day>\d{1,2}) *(?:-|\.|/) *(?P<month>january|february|march|april|may|june|july|august|september|october|november|december|sept|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec) *(?:-|\.|/) *(?P<year>\d{2,5})$", flags=re.I)

        self.text_mdy_regex = re.compile(r"^(?P<month>january|february|march|april|may|june|july|august|september|october|november|december|sept|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec) *(?:-|\.|/) *(?P<day>\d{1,2}) *(?:-|\.|/) *(?P<year>\d{2,5})$", flags=re.I)


        self.dmy_regex = re.compile(r"^(?:(?:(?P<day>\d{1,2}) +(of +)?)?(?P<month>january|february|march|april|may|june|july|august|september|october|november|december|sept|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\.? +)?(?P<year>\d{1,5})(?P<suffix>s?)\/?(?: *(?P<bcsuffix>[A-Z\.]+)?)$", flags=re.I)

        self.mdy_regex = re.compile(r"^(?P<month>january|february|march|april|may|june|july|august|september|october|november|december|sept|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)?\.? *(?P<day>\d{1,2})? +(?P<year>\d{1,5})(?P<suffix>s?)\/?(?: *(?P<bcsuffix>[A-Z\.]+)?)$", flags=re.I)


        self.dm_regex = re.compile(r"^(?P<day>\d{1,2}) +(of +)?(?P<month>january|february|march|april|may|june|july|august|september|october|november|december|sept|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\.?(?: *(?P<bcsuffix>[A-Z\.]+)?)$", flags=re.I)

        self.md_regex = re.compile(r"^(?P<month>january|february|march|april|may|june|july|august|september|october|november|december|sept|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\.? +(?P<day>\d{1,2})(?: *(?P<bcsuffix>[A-Z\.]+)?)$", flags=re.I)

        self.th_regex = re.compile(r"(?:(?<=\d)|(?<=\d ))(?:th|nd|rd|st)", flags=re.I)

        self.trans_month_dict = {
            "jan": "january",
            "feb": "february",
            "mar": "march",
            "apr": "april",
            #"may": "may",
            "jun": "june",
            "jul": "july",
            "aug": "august",
            "sep": "september",
            "oct": "october",
            "nov": "november",
            "dec": "december",

            "sept": "september",

            "01": "january",
            "02": "february",
            "03": "march",
            "04": "april",
            "05": "may",
            "06": "june",
            "07": "july",
            "08": "august",
            "09": "september",
            "10": "october",
            "11": "november",
            "12": "december",

            "1": "january",
            "2": "february",
            "3": "march",
            "4": "april",
            "5": "may",
            "6": "june",
            "7": "july",
            "8": "august",
            "9": "september",
        }

        self.trans_day_dict = {
            "mon": "monday",
            "tue": "tuesday",
            "wed": "wednesday",
            "thu": "thursday",
            "fri": "friday",
            "sat": "saturday",
            "sun": "sunday",
        }

        self.cardinal = Cardinal()
        self.ordinal = Ordinal()
    
    def convert(self, token: str) -> str:

        dmy = True

        prefix = None
        day = None
        month = None
        year = None
        suffix = None

        token = self.filter_regex.sub("", token).strip()

        match = self.th_regex.search(token)
        if match:
            token = token[:match.span()[0]] + token[match.span()[1]:]

        match = self.day_regex.match(token)
        if match:
            prefix = self.get_prefix(match.group("prefix"))
            token = token[match.span()[1]:].strip()

        if token.lower().startswith("the "):
            token = token[4:]

        def construct_output():
            result_list = []
            result_list.append(prefix)

            if dmy:
                if day:
                    result_list.append("the")
                    result_list.append(day)
                    result_list.append("of")
                result_list.append(month)
            else:
                result_list.append(month)
                result_list.append(day)
            result_list.append(year)
            result_list.append(suffix)
            return " ".join([result for result in result_list if result])

        match = self.dm_regex.match(token)
        if not match:
            match = self.md_regex.match(token)
            if match:
                dmy = False
        if match:
            day = self.ordinal.convert(match.group("day"))
            month = self.get_month(match.group("month"))
            try:
                suffix = " ".join([c for c in match.group("bcsuffix").lower() if c not in (" ", ".")])
            except (IndexError, AttributeError):
                pass
            return construct_output()

        match = self.dash_date_mdy_regex.match(token) or self.dash_date_ymd_regex.match(token) or self.text_dmy_regex.match(token) or self.text_ymd_regex.match(token) or self.text_mdy_regex.match(token)
        if match:
            day, month, year = match.group("day"), match.group("month"), match.group("year")
            
            try:
                if match.group(0).startswith(month) and int(day) > 12 or prefix and match.group(0).endswith(year) and int(month) <= 12:
                    dmy = False

                if int(month) > 12:
                    month, day = day, month
            except ValueError:
                pass

            month, year = self.get_month(month), self.convert_year(year)
            if day:
                day = self.ordinal.convert(day)
            return construct_output()

        match = self.dmy_regex.match(token)
        if not match:
            match = self.mdy_regex.match(token)
            if match:
                dmy = False
        if match:
            if match.group("day"):
                day = self.ordinal.convert(match.group("day"))
            month = self.get_month(match.group("month"))
            if match.group("suffix"):
                year = self.convert_year(match.group("year"), cardinal=False)
            else:
                year = self.convert_year(match.group("year"))
            try:
                suffix = " ".join([c for c in match.group("bcsuffix").lower() if c not in (" ", ".")])
            except (IndexError, AttributeError):
                pass
            return construct_output()

        return token

    def get_prefix(self, prefix):
        if prefix is None:
            return prefix
        if prefix.lower() in self.trans_day_dict:
            return self.trans_day_dict[prefix.lower()]
        return prefix.lower()

    def convert_year(self, token: str, cardinal:bool = True) -> str:
        if token == "00":
            return "o o"

        if token[-3:-1] == "00":
            result = self.cardinal.convert(token)
            if not cardinal:
                if result[-1] == "x":
                    result += "e"
                result += "s"
            return result

        result_list = []
        if token[-4:-2]:
            result_list.append(self.cardinal.convert(token[-4:-2]))
        if token[-2:] == "00":
            result_list.append("hundred" if cardinal else "hundreds")
            return " ".join(result_list)

        if token[-2:-1] == "0":
            if len(token) == 3:
                result_list.append("hundred")
            else:
                result_list.append("o")

        year_text = self.cardinal.convert(token[-2:])

        if not cardinal:
            if year_text.endswith("y"):
                year_text = year_text[:-1] + "ies"
            else:
                year_text += "s" if year_text[-1] != "x" else "es"
        result_list.append(year_text)

        return " ".join(result_list)

    def get_month(self, token: str) -> str:
        if not token:
            return token
        if token.lower() in self.trans_month_dict:
            return self.trans_month_dict[token.lower()]
        return token.lower()
