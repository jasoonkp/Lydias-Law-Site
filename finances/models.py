from django.db import models
from django.conf import settings

class Payment(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="payments", db_index=True)
    amount = models.PositiveIntegerField(help_text="minor units (cents)")
    currency = models.CharField(max_length=3, default="USD")
    description = models.CharField(max_length=255, null=True, blank=True)
    
    class Status(models.TextChoices):
        SUCCESS = "SUCCESS", "Success"
        PENDING = "PENDING", "Pending"
        REFUNDED = "REFUNDED", "Refunded"
        FAILED = "FAILED", "Failed"

    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    paid_at = models.DateTimeField(null=True, blank=True)
