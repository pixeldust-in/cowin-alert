from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse_lazy

from .managers import AlertRequestManager
from .mixins import AbstractBaseSet


class User(AbstractUser, AbstractBaseSet):
    pass


class AlertRequest(AbstractBaseSet):
    email = models.EmailField()
    from_date = models.DateField()
    to_date = models.DateField()
    pincode = models.CharField(max_length=6)
    alerts_enabled = models.BooleanField(default=True)

    objects = AlertRequestManager.as_manager()

    def __str__(self):
        return f"from: {self.from_date} - to:{self.to_date} - Pincode: {self.pincode}"

    def unsubscribe(self):
        self.alerts_enabled = False
        self.save()

    def get_unsubscribe_url(self):
        return reverse_lazy("src.core:unsubscribe", kwargs={"uuid": self.uuid})


class CowinCenter(AbstractBaseSet):
    center_id = models.PositiveIntegerField()
    pincode = models.CharField(max_length=6)
    name = models.CharField(max_length=1024)
    state_name = models.CharField(max_length=255, null=True, blank=True)
    district_name = models.CharField(max_length=255, null=True, blank=True)
    block_name = models.CharField(max_length=255, null=True, blank=True)


class CowinSession(AbstractBaseSet):
    center = models.ForeignKey(
        CowinCenter, related_name="sessions", on_delete=models.CASCADE
    )
    session_id = models.UUIDField(unique=True)
    date = models.DateField()
    available_capacity = models.CharField(max_length=100, null=True, blank=True)
    min_age_limit = models.CharField(max_length=2, null=True)
    vaccine = models.CharField(max_length=255, null=True, blank=True)
    slots = models.JSONField(default=dict)


class SessionAlertMap(AbstractBaseSet):
    alert_request = models.ForeignKey(
        AlertRequest, on_delete=models.CASCADE, related_name="alerts_sent"
    )
    session = models.ForeignKey(
        CowinSession, on_delete=models.CASCADE, related_name="alerts_sent"
    )

    class Meta:
        unique_together = (
            "alert_request",
            "session",
        )
