# notifications/models.py
from django.conf import settings
from django.db import models

import random, string # to generate confirmation numbers
from datetime import timedelta

# Notifications model

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


# ------- Appointments model ------
# Stores appointments only
class Appointments(models.Model):
    user_id = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="appointments")
    start_time = models.DateTimeField()
    duration = models.DurationField(default=timedelta(minutes=15))
    comments = models.TextField(blank=True, null=True)
    approved = models.BooleanField(default=False)
    calendar_api_id = models.CharField(max_length=255, blank=True, null=True)

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        CONFIRMED = "CONFIRMED", "Confirmed"
        CANCELLED = "CANCELLED", "Cancelled"
        NO_SHOW = "NO_SHOW", "No-show"
        COMPLETED = "COMPLETED", "Completed"
        
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)

    # Admin cancellation (LLW-63)
    cancellation_reason = models.TextField(blank=True, null=True)
    cancelled_at = models.DateTimeField(blank=True, null=True)

    # Valid status transitions (LLW-64)
    ALLOWED_STATUS_TRANSITIONS = {
        Status.PENDING: {Status.CONFIRMED, Status.CANCELLED},
        Status.CONFIRMED: {Status.COMPLETED, Status.NO_SHOW, Status.CANCELLED},
        Status.CANCELLED: set(),
        Status.NO_SHOW: set(),
        Status.COMPLETED: set(),
    }

    @classmethod
    def can_transition_status(cls, from_status: str, to_status: str) -> bool:
        return to_status in cls.ALLOWED_STATUS_TRANSITIONS.get(from_status, set())


    # Creating confirmation numbers function
    def create_confirmation_number():
        confirmation_number = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        return(confirmation_number.upper())

    # Calendly Appointment extensions:
    calendly_event_uri = models.URLField(unique=True, null=True, blank=True,)
    calendly_event_name = models.CharField(max_length=255, null=True, blank=True)
    calendly_event_status = models.CharField(max_length=50, null=True, blank=True)
    calendly_created_at = models.DateTimeField(null=True, blank=True)
    calendly_updated_at = models.DateTimeField(null=True, blank=True)
    calendly_location_type = models.CharField(max_length=100, null=True, blank=True)
    calendly_join_url = models.URLField(null=True, blank=True)
    calendly_organization_uri = models.URLField(null=True, blank=True)
    calendly_host_email = models.EmailField(null=True, blank=True)
    confirmation_number = models.CharField(max_length=8, unique=True, null=True, blank=True, default=create_confirmation_number)
    

    # To-string method that converts it to smt like "Appointment: (Nov 11, 2025 - 9:00 PM) - CONFIRMED"
    # If you want to change formatting, use this: 
    # https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
    def __str__(self):
        format_date_time = self.start_time.strftime('%b %d, %Y - %I:%M %p')
        return f"Appointment: ({format_date_time}) - {self.status}"

    # Ordered by newest first
    class Meta:
        ordering = ["-start_time"]


# ------- Invitee model ---------
# Stores the people attending appointment
class Invitee(models.Model):
    appointment = models.ForeignKey(
        Appointments, on_delete=models.CASCADE, related_name='invitees'
    )
    calendly_invitee_uri = models.URLField(unique=True, null=True, blank=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # US numbers only
    status = models.CharField(max_length=50, default="active")
    canceled = models.BooleanField(default=False)
    cancellation_reason = models.TextField(null=True, blank=True)
    reschedule_url = models.URLField(null=True, blank=True)
    calendly_created_at = models.DateTimeField(null=True, blank=True) # added again in case of Calendly event change (reschedule)
    calendly_updated_at = models.DateTimeField(null=True, blank=True) # added again in case of Calendly event change

    def __str__(self):
        return f"{self.name} ({self.email})"


class CalendlyOAuthToken(models.Model):
    """
    Stores Calendly OAuth tokens for server-to-server API usage.
    This is scaffolded for future production use; local dev can keep the API disabled.
    """

    access_token = models.TextField()
    refresh_token = models.TextField(blank=True, null=True)
    token_type = models.CharField(max_length=20, default="Bearer")
    scope = models.TextField(blank=True, null=True)
    expires_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
