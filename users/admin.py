# users/admin.py
from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("user_id", "first_name","last_name", "email", "created_at")  # adjust to your fields
    list_filter = ("created_at",)
    search_fields = ("last_name", "email")
    ordering = ("created_at",)
