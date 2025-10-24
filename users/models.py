from django.db import models

# Create your models here.
class User(models.Model):
    class Role(models.TextChoices):
        GUEST = "GUEST", "Guest"
        CLIENT = "CLIENT", "Client"
        ADMIN = "ADMIN", "Admin"

    user_id = models.AutoField(primary_key=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.GUEST)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    password_hash = models.CharField(max_length=255)
    payment_provider = models.CharField(max_length=50, blank=True, null=True)
    provider_customer_id = models.IntegerField(blank=True, null=True)
    retainer_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"