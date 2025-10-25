from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings

class UserManager(BaseUserManager):
    use_in_migrations = True
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Django hashes the password securely
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, **extra_fields)
    
# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField("email address", unique=True)
    class Role(models.TextChoices):
        GUEST = "GUEST", "Guest"
        CLIENT = "CLIENT", "Client"
        ADMIN = "ADMIN", "Admin"

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.GUEST)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    payment_provider = models.CharField(max_length=50, blank=True, null=True)
    provider_customer_id = models.CharField(max_length=100,blank=True, null=True)
    retainer_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS=[]

    objects = UserManager()

# Admin Table
class AdminProfile(models.Model):
    user = models.OneToOneField( # 1-1 relationship with user table
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, # when user is deleted, all associated AdminProfile rows are deleted as well
        related_name="admin_profile",
    )
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.email} ({self.role})"