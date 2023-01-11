from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.db import (
    models,
    connection
)


class TimeStampMixin(models.Model):
    created = models.DateTimeField(
        _("created"),
        auto_now_add=True,
        help_text=_("Automatic registration of record creation time "
                    "in the database."),
    )
    modified = models.DateTimeField(
        _("modified"),
        auto_now=True,
        help_text=_("Automatic registration of record modification time "
                    "in the database."),
    )

    @admin.display(description=_("created"), ordering=("-created"))
    def get_gregorian_created(self):
        return self.created.strftime("%Y-%m-%d")

    @admin.display(description=_("modified"), ordering=("-modified"))
    def get_gregorian_modified(self):
        return self.modified.strftime("%Y-%m-%d")

    class Meta:
        abstract = True


class TruncateMixin:
    @classmethod
    def truncate(cls):
        with connection.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE '{0}' CASCADE".format(cls._meta.db_table))  # noqa
