
from singleton_decorator import singleton

import re

from .Cardinal import Cardinal

@singleton
class Time:
    def __init__(self):
        super().__init__()

        self.filter_regex = re.compile(r"[. ]")

        self.time_regex = re.compile(r"^(?P<hour>\d{1,2}) *((?::|.) *(?P<minute>\d{1,2}))? *(?P<suffix>[a-zA-Z\. ]*)$", flags=re.I)
        self.full_time_regex = re.compile(r"^(?:(?P<hour>\d{1,2}) *:)? *(?P<minute>\d{1,2})(?: *: *(?P<seconds>\d{1,2})(?: *. *(?P<milliseconds>\d{1,2}))?)? *(?P<suffix>[a-zA-Z\. ]*)$", flags=re.I)
        self.ampm_time_regex = re.compile(r"^(?P<suffix>[a-zA-Z\. ]*)(?P<hour>\d{1,2})", flags=re.I)

        self.cardinal = Cardinal()

    def convert(self, token: str) -> str:

        token = token.strip()

        result_list = []

        match = self.time_regex.match(token)
        if match:
            hour, minute, suffix = match.group("hour"), match.group("minute"), match.group("suffix")

            ampm = self.filter_regex.sub("", suffix).lower().startswith(("am", "pm"))

            if ampm:
                result_list.append(self.cardinal.convert(self.modulo_hour(hour)))
            else:
                result_list.append(self.cardinal.convert(hour))

            if minute and minute != "00":
                if minute[0] == "0":
                    result_list.append("o")
                result_list.append(self.cardinal.convert(minute))

            elif not ampm:
                if int(hour) > 12 or int(hour) == 0:
                    result_list.append("hundred")
                else:
                    result_list.append("o'clock")

            if suffix:
                result_list += [c for c in suffix.lower() if c not in (" ", ".")]
            
            return " ".join(result_list)

        match = self.full_time_regex.match(token)
        if match:
            hour, minute, seconds, milliseconds, suffix = match.group("hour"), match.group("minute"), match.group("seconds"), match.group("milliseconds"), match.group("suffix")

            if hour:
                result_list.append(self.cardinal.convert(hour))
                result_list.append("hour" if int(hour) == 1 else "hours")
            if minute:
                result_list.append(self.cardinal.convert(minute))
                result_list.append("minute" if int(minute) == 1 else "minutes")
            if seconds:
                if not milliseconds:
                    result_list.append("and")
                result_list.append(self.cardinal.convert(seconds))
                result_list.append("second" if int(seconds) == 1 else "seconds")
            if milliseconds:
                result_list.append("and")
                result_list.append(self.cardinal.convert(milliseconds))
                result_list.append("millisecond" if int(milliseconds) == 1 else "milliseconds")
            if suffix:
                result_list += [c for c in suffix.lower() if c not in (" ", ".")]
            
            return " ".join(result_list)

        match = self.ampm_time_regex.match(token)
        if match:
            hour, suffix = match.group("hour"), match.group("suffix")

            ampm = self.filter_regex.sub("", suffix).lower().startswith(("am", "pm"))

            if ampm:
                result_list.append(self.cardinal.convert(self.modulo_hour(hour)))
            else:
                result_list.append(self.cardinal.convert(hour))
            result_list += [c for c in suffix.lower() if c not in (" ", ".")]
            return " ".join(result_list)

        return token

    def modulo_hour(self, hour: str) -> str:
        if hour == "12":
            return hour
        return str(int(hour) % 12)
