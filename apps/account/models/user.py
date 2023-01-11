from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.postgres.fields import (
    CICharField,
    CIEmailField
)
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
    RegexValidator
)

from apps.account.repository.manager import UserManager
from painless.helper.enums import RegexPatternEnum
from painless.models import (
    TimeStampMixin,
    TruncateMixin
)


class User(AbstractUser,
           TimeStampMixin,
           TruncateMixin):
    REQUIRED_FIELDS = list()
    # username field must be case-insensitive, so override this filed.
    username_validator = UnicodeUsernameValidator()
    username = CICharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    # email field must be unique and case-insensitive, so override this filed.
    email = CIEmailField(
        _("email address"),
        unique=True,
        help_text=_("User's email address"),
        error_messages={
            "unique": _("A user with that email address already exists."),
        },
    )
    phone_number = models.CharField(
        _("phone number"),
        unique=True,
        max_length=13,
        validators=[RegexValidator(RegexPatternEnum.Iran_phone_number.value),
                    MinLengthValidator(11),
                    MaxLengthValidator(13)],
        help_text=_("User's phone number"),
        error_messages={
            "unique": _("A user with that phone number already exists."),
        },
    )
    is_verified = models.BooleanField(
        _("is verified"),
        default=False,
        help_text=_("Whether this user is verified or not"),
    )

    dal = UserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("user")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)
        self.username = self.username.lower()

    def __str__(self):
        return f"{self.username}"

    def __repr__(self):
        return f"{self.username}"
