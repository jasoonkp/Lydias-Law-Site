from django.contrib import admin

from .models import Appointments, CalendlyOAuthToken, Invitee

@admin.register(Appointments)
class AppointmentsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user_id",
        "start_time",
        "duration",
        "status",
        "approved",
        "confirmation_number",
        "calendar_api_id",
        "calendly_event_name",
        "calendly_event_status",
    )
    list_filter = ("status", "approved", "start_time")
    search_fields = ("user_id__email", "comments", "calendar_api_id", "confirmation_number", "calendly_event_uri")
    ordering = ("-start_time",)
    readonly_fields = (
        "confirmation_number",
        "calendly_created_at",
        "calendly_updated_at",
    )

    fieldsets = (
        ("Core", {"fields": ("user_id", "start_time", "duration", "status", "approved", "comments")}),
        ("Cancellation", {"fields": ("cancellation_reason", "cancelled_at")}),
        (
            "Calendly",
            {
                "fields": (
                    "calendar_api_id",
                    "calendly_event_uri",
                    "calendly_event_name",
                    "calendly_event_status",
                    "calendly_created_at",
                    "calendly_updated_at",
                    "calendly_location_type",
                    "calendly_join_url",
                    "calendly_organization_uri",
                    "calendly_host_email",
                )
            },
        ),
        ("Confirmation", {"fields": ("confirmation_number",)}),
    )
    
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


@admin.register(CalendlyOAuthToken)
class CalendlyOAuthTokenAdmin(admin.ModelAdmin):
    """
    Stored for future live Calendly integration. Tokens are sensitive: keep read-only
    and avoid showing raw values in the changelist.
    """

    list_display = ("id", "token_type", "expires_at", "created_at", "updated_at")
    ordering = ("-updated_at",)
    readonly_fields = ("access_token", "refresh_token", "token_type", "scope", "expires_at", "created_at", "updated_at")

    def has_add_permission(self, request):
        return False


