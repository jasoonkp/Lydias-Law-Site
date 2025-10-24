from django.db import models

# Create your models here.
class Notification(models.Model):
    notif_id = models.AutoField(primary_key=True) # Primary Key

    user_id = models.ForeignKey(
        'users.User',       
        on_delete=models.CASCADE, # deletes notifications of user if user is deleted
        null=True, # allows null for guest notifications
        blank=True,
        related_name='notifications'
    )

    # Notification delivery channel
    class Channel(models.TextChoices):
        EMAIL = 'EMAIL', 'Email'
        SMS = 'SMS', 'SMS'

    channel = models.CharField(
        max_length=10,
        choices=Channel.choices
    )

    # Type of notification
    class Type(models.TextChoices):
        APPT_CONFIRM = 'APPT_CONFIRM', 'Appointment Confirmation'
        APPT_REMINDER = 'APPT_REMINDER', 'Appointment Reminder'
        INVOICE_ISSUED = 'INVOICE_ISSUED', 'Invoice Issued'
        PAYMENT_RECEIPT = 'PAYMENT_RECEIPT', 'Payment Receipt'
        PASSWORD_RESET = 'PASSWORD_RESET', 'Password Reset'

    # Sets different types of notifications as a field
    type = models.CharField(
        max_length=30,
        choices=Type.choices
    )

    # Timestamp when notification was sent
    sent_at = models.DateTimeField()

    # Status of the notification
    class Status(models.TextChoices):
        SENT = 'SENT', 'Sent'
        FAILED = 'FAILED', 'Failed'

    # Sets the different types of statuses as a field
    status = models.CharField(
        max_length=10,
        choices=Status.choices
    )

    # Prints notification, who it was sent to, and how
    def __str__(self):
        return f"{self.get_type_display()} to {self.user or 'Guest'} via {self.channel}"

