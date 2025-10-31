from django.contrib import admin

from django.contrib import admin
from .models import Appointments

@admin.register(Appointments)
class AppointmentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'start_time', 'duration', 'approved')
    list_filter = ('approved', 'start_time')
    search_fields = ('user_id__username', 'comments', 'calendar_api_id')
    ordering = ('-start_time',)
    readonly_fields = ('calendar_api_id',)

    def __str__(self):
        return f"{self.user_id} - {self.start_time}"