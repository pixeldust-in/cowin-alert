from django.contrib import admin

from . import models

# Register your models here.


@admin.register(models.AlertRequest)
class AlertRequestAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.AlertRequest._meta.fields]
    search_fields = ["name", "mobile", "email"]


class CowinSessionInline(admin.StackedInline):
    model = models.CowinSession
    extra = 0


@admin.register(models.CowinCenter)
class CowinCenterAdmin(admin.ModelAdmin):
    list_display = [
        "uuid",
        "center_id",
        "name",
        "district_name",
        "state_name",
        "pincode",
    ]
    readonly_fields = (
        "uuid",
        "center_id",
        "name",
        "block_name",
        "district_name",
        "state_name",
        "pincode",
    )

    inlines = (CowinSessionInline,)


@admin.register(models.CowinSession)
class CowinSessionAdmin(admin.ModelAdmin):
    list_display = (
        "center",
        "session_id",
        "date",
        "available_capacity",
        "min_age_limit",
        "vaccine",
        "slots",
    )
