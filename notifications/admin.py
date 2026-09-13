from django.contrib import admin
from .models import Trigger, Template


@admin.register(Trigger)
class TriggerAdmin(admin.ModelAdmin):
    list_display = ("code", "name")


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ("trigger", "channel", "subject", "is_active")
    list_editable = ("is_active",)
    list_filter = ("channel", "trigger")
