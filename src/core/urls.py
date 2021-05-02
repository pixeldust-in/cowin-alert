from django.urls import path

from . import apis

app_name = "core"


urlpatterns = [
    path("api/register", apis.alert_registrations),
    path("unsubscribe/<uuid:uuid>", apis.unsubscribe),
]
