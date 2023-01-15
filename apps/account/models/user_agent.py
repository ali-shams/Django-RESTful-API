from django.db import models
from django.utils.translation import gettext_lazy as _
from knox.models import AuthToken

from apps.account.repository.manager import UserAgentDataAccessLayerManager


class UserAgent(models.Model):
    user_agent = models.CharField(
        _("user agent"),
        max_length=255,
        help_text=_("User agent"),
    )
    auth_token = models.OneToOneField(
        AuthToken,
        verbose_name=_('auth token'),
        related_name='user_agent',
        on_delete=models.CASCADE,
        help_text=_('The auth token this user agent belongs to'),
    )

    dal = UserAgentDataAccessLayerManager()

    class Meta:
        verbose_name = _("user agent")
        verbose_name_plural = _("user agents")

    def __str__(self):
        return f"{self.user_agent}"

    def __repr__(self):
        return f"{self.user_agent}"
