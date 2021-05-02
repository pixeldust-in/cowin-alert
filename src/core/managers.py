from django.db import models
from django.utils import timezone


class AlertRequestManager(models.QuerySet):
    def active(self):
        return self.filter(alerts_enabled=True)

    def get_for_today(self):
        today = timezone.localdate()
        return self.active().filter(from_date__lte=today, to_date__gte=today)
