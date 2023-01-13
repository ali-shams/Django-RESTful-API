from enum import Enum


class RegexPatternEnum(Enum):
    Iran_phone_number = r"(\+989\d{9})|(09\d{9})$"
    International_phone_number = r"^(\(?\+?[0-9]*\)?)?[0-9_\- \(\)]*$"


class RegexOperatorPattern(Enum):
    # HamraheAval: 091[0-9] | 099[0-6]
    HamraheAval = r"(\+9891[0-9]\d{7})|(091[0-9]\d{7})$"
    # Irancell: 090[0-5] | 093[0]|[3]|[5-9]
    Irancell = r"(\+9890[0-5]\d{7})|(090[0-5]\d{7})|(\+9893([0]|[3]|[5-9])\d{7})|(093([0]|[3]|[5-9])\d{7})$"
    # Rightel: 092[0-3]
    Rightel = r"(\+9892[0-3]\d{7})|(092[0-3]\d{7})$"
    # ShatelMobile: 0998
    ShatelMobile = r"(\+98998\d{7})|(0998\d{7})$"
    # Samantel: 0999
    Samantel = r"(\+98999\d{7})|(0999\d{7})$"
    # Taliya: 0932
    Taliya = "(\+98932\d{7})|(0932\d{7})$"
