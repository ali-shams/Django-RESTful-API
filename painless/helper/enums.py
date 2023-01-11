from enum import Enum


class RegexPatternEnum(Enum):
    Iran_phone_number = r"^(\+98|0)?9\d{9}$"
    International_phone_number = r"^(\(?\+?[0-9]*\)?)?[0-9_\- \(\)]*$"
