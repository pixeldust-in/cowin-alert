from django.contrib import admin

from . import models

# Register your models here.


@admin.register(models.AlertRequest)
class AlertRequestAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.AlertRequest._meta.fields]
    search_fields = ["name", "mobile", "email"]


@admin.register(models.CowinCenter)
class CowinCenterAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.CowinCenter._meta.fields]


@admin.register(models.CowinSession)
class CowinSessionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.CowinSession._meta.fields]
