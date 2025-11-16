from datetime import timedelta
from django.http import JsonResponse, HttpResponseBadRequest
from django.utils.dateparse import parse_datetime
from django.views.decorators.csrf import csrf_exempt

from .models import Appointments, Invitee
from users.models import User
import json


@csrf_exempt
def calendly_webhook(request):
    if request.method != "POST":
        return HttpResponseBadRequest("POST only")

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    print(">>> Calendly webhook HIT")
    print(">>> Parsed payload:", payload)

    event_type = payload.get("event")  # e.g. "invitee.created"
    data = payload.get("payload") or {}

    if event_type != "invitee.created":
        return JsonResponse({"status": "ignored", "reason": "unsupported event"})

    # ---- Extract scheduled event + invitee data ----
    scheduled_event = data.get("scheduled_event", {})  # dict with event info
    invitee_uri = data.get("uri")                      # string

    if not scheduled_event:
        return HttpResponseBadRequest("Missing scheduled_event data")

    calendly_event_uri = scheduled_event.get("uri")
    if not calendly_event_uri:
        return HttpResponseBadRequest("Missing event uri")

    # Start / end time
    start_time_str = scheduled_event.get("start_time")
    end_time_str = scheduled_event.get("end_time")

    start_time = parse_datetime(start_time_str) if start_time_str else None
    end_time = parse_datetime(end_time_str) if end_time_str else None
    duration = (end_time - start_time) if (start_time and end_time) else timedelta(minutes=30)

    # ---- Find the host user (attorney) from event_memberships ----
    event_memberships = scheduled_event.get("event_memberships", []) or []
    host_email = None
    if event_memberships:
        host_email = event_memberships[0].get("user_email")  # "jasonprakash@csus.edu" in your logs

    host_user = None
    if host_email:
        # Look up existing user by email (your model uses email as username)
        host_user = User.objects.filter(email=host_email).first()

    # Fallback: first superuser (e.g., Lydia/admin)
    if host_user is None:
        host_user = User.objects.filter(is_superuser=True).first()

    if host_user is None:
        # Don't create Appointment if we can't associate it with a valid user
        return HttpResponseBadRequest("No host user found; create an admin user with the Calendly host email.")

    location = scheduled_event.get("location", {}) or {}

    # ---- Build defaults for new appointments (includes required user_id) ----
    defaults = {
        "user_id": host_user,
        "start_time": start_time,
        "duration": duration,
        "status": Appointments.Status.CONFIRMED,
        "calendar_api_id": calendly_event_uri,
        "calendly_event_name": scheduled_event.get("name"),
        "calendly_event_status": scheduled_event.get("status", "active"),
        "calendly_created_at": parse_datetime(scheduled_event.get("created_at")) if scheduled_event.get("created_at") else None,
        "calendly_updated_at": parse_datetime(scheduled_event.get("updated_at")) if scheduled_event.get("updated_at") else None,
        "calendly_location_type": location.get("type"),
        "calendly_join_url": location.get("join_url"),  # may be None for physical
        "calendly_organization_uri": None,
        "calendly_host_email": host_email,
    }

    # ---- Create or update Appointment ----
    appt, created = Appointments.objects.get_or_create(
        calendly_event_uri=calendly_event_uri,
        defaults=defaults,
    )

    if not created:
        # Update existing appointment with latest info
        for field, value in defaults.items():
            setattr(appt, field, value)
        appt.save()

    # ---- Create Invitee record ----
    Invitee.objects.get_or_create(
        calendly_invitee_uri=invitee_uri,
        defaults={
            "appointment": appt,
            "name": data.get("name", ""),
            "email": data.get("email", ""),
            "phone_number": data.get("text_reminder_number"),
            "status": data.get("status", "active"),
            "canceled": data.get("rescheduled", False),
            "cancellation_reason": None,
            "reschedule_url": data.get("reschedule_url"),
            "calendly_created_at": parse_datetime(data.get("created_at")) if data.get("created_at") else None,
            "calendly_updated_at": parse_datetime(data.get("updated_at")) if data.get("updated_at") else None,
        },
    )

    return JsonResponse({"status": "ok"})
