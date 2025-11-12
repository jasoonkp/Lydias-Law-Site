from django.contrib import admin

from django.contrib import admin
from .models import Appointments
from .models import Invitee

@admin.register(Appointments)
class AppointmentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'start_time', 'duration', 'approved', 'confirmation_number')
    list_filter = ('approved', 'start_time')
    search_fields = ('user_id__username', 'comments', 'calendar_api_id')
    ordering = ('-start_time',)
    readonly_fields = ('calendar_api_id', 'confirmation_number')

    def __str__(self):
        return f"{self.user_id} - {self.start_time}"
    
@admin.register(Invitee)
class InviteeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone_number',
                    'get_start_time', 'get_confirmation_number')
    search_fields = ('name', 'email', 'phone_number', 'appointment__confirmation_number')

    def get_start_time(self, obj):
        return obj.appointment.start_time
    get_start_time.short_description = 'Appointment Time'

    def get_confirmation_number(self, obj):
        return obj.appointment.confirmation_number
    get_confirmation_number.short_description = 'Confirmation #'

