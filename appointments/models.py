# notifications/models.py
from django.conf import settings
from django.db import models


class Notification(models.Model):
    # Let Django create the primary key `id` automatically.
    # If you really want a custom name, keep your AutoField, but default `id` is standard.

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,          # works with your custom users.User
        on_delete=models.CASCADE,          # delete notifications if user is deleted
        null=True,                         # allow guest notifications
        blank=True,
        related_name="notifications",
    )

    class Channel(models.TextChoices):
        EMAIL = "EMAIL", "Email"
        SMS = "SMS", "SMS"

    channel = models.CharField(
        max_length=10,
        choices=Channel.choices,
    )

    class Type(models.TextChoices):
        APPT_CONFIRM = "APPT_CONFIRM", "Appointment Confirmation"
        APPT_REMINDER = "APPT_REMINDER", "Appointment Reminder"
        INVOICE_ISSUED = "INVOICE_ISSUED", "Invoice Issued"
        PAYMENT_RECEIPT = "PAYMENT_RECEIPT", "Payment Receipt"
        PASSWORD_RESET = "PASSWORD_RESET", "Password Reset"

    type = models.CharField(
        max_length=30,
        choices=Type.choices,
        db_index=True,
    )

    # When this record is created (i.e., we sent/attempted to send)
    sent_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Status(models.TextChoices):
        SENT = "SENT", "Sent"
        FAILED = "FAILED", "Failed"

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.SENT,
        db_index=True,
    )

    # Optional metadata for tracing with providers (Twilio/Postmark/Calendly, etc.)
    provider = models.CharField(max_length=50, blank=True, null=True)              # e.g., 'twilio', 'postmark'
    provider_message_id = models.CharField(max_length=128, blank=True, null=True)  # their message/event id
    error_message = models.TextField(blank=True, null=True)                        # store failure reason if any
    payload = models.JSONField(default=dict, blank=True)                           # what we sent (sanitized)

    # For guest notifications (no user), keep a snapshot of where it went:
    target_email = models.EmailField(blank=True, null=True)
    target_phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        who = self.user.email if self.user else (self.target_email or self.target_phone or "Guest")
        return f"{self.get_type_display()} to {who} via {self.channel} [{self.status}]"

    class Meta:
        ordering = ["-sent_at"]
        indexes = [
            models.Index(fields=["channel", "status"]),
            models.Index(fields=["type", "sent_at"]),
        ]
