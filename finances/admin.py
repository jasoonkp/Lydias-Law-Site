from django.contrib import admin
from .models import Payment
from .models import Invoice

# Register your models here.

# Payment Table
admin.site.register(Payment)

# Invoice Table
@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "amount", "paid", "created_at")
    list_filter = ("paid", "created_at")
    search_fields = ("email", "first_name", "last_name")
