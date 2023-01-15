import re
from abc import ABC, abstractmethod

from ..helper.enums import RegexOperatorPattern


def getOTP(phone_number):
    operator_name = "Other"
    for operator in RegexOperatorPattern:
        if re.compile(operator.value).match(phone_number):
            operator_name = operator.name
            break
    formats = {
        "HamraheAval": HamraheAvalPhoneNumber,
        "Irancell": IrancellPhoneNumber,
        "Rightel": RightelPhoneNumber,
        "ShatelMobile": ShatelMobilePhoneNumber,
        "Samantel": SamantelPhoneNumber,
        "Taliya": TaliyaPhoneNumber,
        "Other": OtherPhoneNumber,
    }
    result = formats[operator_name](phone_number)
    return result.call_send_otp()


# ############################### #
#            Creator              #
# ############################### #
class Creator(ABC):
    def __init__(self, phone_number):
        self.phone_number = phone_number

    @abstractmethod
    def factory_method(self):
        ...

    def call_send_otp(self):
        product = self.factory_method()
        result = product.send_otp(self.phone_number)
        return result


# ############################### #
#        ConcreteCreator          #
# ############################### #
class HamraheAvalPhoneNumber(Creator):
    def factory_method(self):
        return HamraheAval()


class IrancellPhoneNumber(Creator):
    def factory_method(self):
        return Irancell()


class RightelPhoneNumber(Creator):
    def factory_method(self):
        return Rightel()


class ShatelMobilePhoneNumber(Creator):
    def factory_method(self):
        return ShatelMobile()


class SamantelPhoneNumber(Creator):
    def factory_method(self):
        return Samantel()


class TaliyaPhoneNumber(Creator):
    def factory_method(self):
        return Taliya()


class OtherPhoneNumber(Creator):
    def factory_method(self):
        return Other()


# ############################### #
#             Product             #
# ############################### #
class Product(ABC):
    @abstractmethod
    def send_otp(self):
        ...


class HamraheAval(Product):
    def send_otp(self, phone_number):
        return f"HamraheAval_{phone_number}"


class Irancell(Product):
    def send_otp(self, phone_number):
        return f"Irancell_{phone_number}"


class Rightel(Product):
    def send_otp(self, phone_number):
        return f"Rightel_{phone_number}"


class ShatelMobile(Product):
    def send_otp(self, phone_number):
        return f"ShatelMobile_{phone_number}"


class Samantel(Product):
    def send_otp(self, phone_number):
        return f"Samantel_{phone_number}"


class Taliya(Product):
    def send_otp(self, phone_number):
        return f"Taliya_{phone_number}"


class Other(Product):
    def send_otp(self, phone_number):
        return f"Other_{phone_number}"
