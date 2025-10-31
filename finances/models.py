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

# Invoice Table
class Invoice(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(    # Foreign key to user who invoice belongs to
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="invoices",
        db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.PositiveIntegerField(help_text="minor units (cents)")
    paid = models.BooleanField(default=False)    

    # Output Readability
    def __str__(self):
        return f"Invoice #{self.id} - User {self.user.id} - ${self.amount}"
    
    class Meta:
        db_table = "invoices"
        ordering = ["-created_at"]