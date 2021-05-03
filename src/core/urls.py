from django.urls import path

from . import apis

app_name = "src.core"


urlpatterns = [
    path("api/register", apis.alert_registrations),
    path("unsubscribe/<uuid:uuid>", apis.unsubscribe, name="unsubscribe"),
]


# if settings.DEBUG:
#     urlpatterns += [
#         path("email", apis.email),
#     ]
