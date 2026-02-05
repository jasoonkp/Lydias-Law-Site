from django.contrib import admin
from .models import Payment, Invoice, StripeWebhookEvent

# Register your models here.

# Payment Table
admin.site.register(Payment)

# Invoice Table
@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "amount", "status", "paid", "created_at")
    list_filter = ("status", "paid", "created_at")
    search_fields = ("email", "first_name", "last_name")


@admin.register(StripeWebhookEvent)
class StripeWebhookEventAdmin(admin.ModelAdmin):
    list_display = ("event_id", "event_type", "received_at")
    list_filter = ("event_type", "received_at")
    search_fields = ("event_id", "event_type")
