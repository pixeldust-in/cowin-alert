from django.contrib.auth.models import AbstractUser

from .mixins import AbstractBaseSet


class User(AbstractUser, AbstractBaseSet):
    pass
