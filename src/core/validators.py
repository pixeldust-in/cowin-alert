import re

from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

mobile_regex = r"^[6-9]\d{9}$"

mobile_validator = RegexValidator(
    re.compile(mobile_regex),
    message=_("Enter a valid 10 digit mobile number"),
    code="invalid",
)
