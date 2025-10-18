from django.contrib import admin

from .models import Client, Mailing, MailingAttempt, Message


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("email", "full_name", "owner")
    list_filter = ("owner",)
    search_fields = ("email", "full_name")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("topic", "owner")
    list_filter = ("owner",)
    search_fields = ("topic", "body")


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("id", "start_time", "end_time", "status", "owner")
    list_filter = ("status", "owner")
    filter_horizontal = ("clients",)


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ("mailing", "attempt_time", "status")
    list_filter = ("status", "attempt_time")
    readonly_fields = ("attempt_time",)
