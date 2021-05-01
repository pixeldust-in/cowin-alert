from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from . import validators
from .mixins import AbstractBaseSet


class User(AbstractUser, AbstractBaseSet):
    pass


class AlertRequest(AbstractBaseSet):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    from_date = models.DateField()
    to_date = models.DateField()
    mobile = models.CharField(
        validators=[validators.mobile_validator], max_length=10, null=True, blank=True
    )
    pincode = models.CharField(max_length=6)
    age = models.PositiveIntegerField(
        validators=[MaxValueValidator(100), MinValueValidator(18)]
    )


class CowinCenter(AbstractBaseSet):
    data = models.JSONField(default=dict)
    center_id = models.PositiveIntegerField()
    pincode = models.CharField(max_length=6)
    name = models.CharField(max_length=1024)


class CowinSession(AbstractBaseSet):
    center = models.ForeignKey(
        CowinCenter, related_name="sessions", on_delete=models.CASCADE
    )
    session_id = models.UUIDField(unique=True, editable=False)
    date = models.DateField()
    available_capacity = models.CharField(max_length=10, null=True, blank=True)
    min_age_limit = models.CharField(max_length=2, null=True)
    vaccine = models.CharField(max_length=255, null=True, blank=True)
    slots = models.JSONField(default=dict)
