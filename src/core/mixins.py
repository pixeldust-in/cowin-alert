from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _


class UuidMixin(models.Model):
    uuid = models.UUIDField(
        _("uuid field"),
        unique=True,
        default=uuid4,
        editable=False,
    )

    class Meta:
        abstract = True


class TimestampMixin(models.Model):
    created = models.DateTimeField(_("created at"), auto_now_add=True)
    modified = models.DateTimeField(_("modified at"), auto_now=True)

    class Meta:
        abstract = True


class AbstractBaseSet(UuidMixin, TimestampMixin):
    """
    Inherit this to have UUID and timestamp fields and default order by creation timestamp.
    And an str implemented to return UUID
    """

    class Meta:
        abstract = True
        ordering = ("-created",)

    def __str__(self):
        return str(self.id)
