from django.shortcuts import render
import json
from datetime import datetime
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.utils.dateparse import parse_datetime
from django.views.decorators.csrf import csrf_exempt

from .models import Appointments, Invitee
from users.models import User


@csrf_exempt  # Calendly can’t send CSRF token
def calendly_webhook(request):
    if request.method != "POST":
        return HttpResponseBadRequest("POST only")
    
    print(">>> Calendly webhook HIT")
    print(">>> Raw body:", request.body)

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    event_type = payload.get("event")  # e.g. "invitee.created"
    # Calendly v2 usually nests data under "payload" or "resource"
    data = payload.get("payload") or payload.get("resource") or {}

    if event_type != "invitee.created":
        # For now we only care about new bookings
        return JsonResponse({"status": "ignored", "reason": "unsupported event"})

    # ---- Extract event info ----
    event = data.get("event", {})
    invitee = data.get("invitee", {})

    calendly_event_uri = event.get("uri")
    if not calendly_event_uri:
        return HttpResponseBadRequest("Missing event uri")

    # Avoid duplicates if Calendly retries the webhook
    appt, created = Appointments.objects.get_or_create(
        calendly_event_uri=calendly_event_uri,
        defaults={}
    )

    # If it already existed, we can just return success
    if not created:
        return JsonResponse({"status": "ok", "detail": "appointment already exists"})

    # Start/end time – adjust keys to match your actual Calendly payload
    start_time_str = event.get("start_time")
    end_time_str = event.get("end_time")

    start_time = parse_datetime(start_time_str) if start_time_str else None
    end_time = parse_datetime(end_time_str) if end_time_str else None
    duration = (end_time - start_time) if (start_time and end_time) else None

    # Determine which user owns this appointment.
    # If Lydia is the only host, you can hardcode her user or use a setting:
    host_email = event.get("extended_assigned_to", [None])[0] or event.get("organizer_email")
    host_user = None

    if host_email:
        host_user, _ = User.objects.get_or_create(
            email=host_email,
            defaults={"username": host_email.split("@")[0]}
        )
    else:
        # fallback: maybe you have a default attorney user
        host_user = User.objects.filter(is_superuser=True).first()

    # Update the appointment fields
    appt.user_id = host_user
    appt.start_time = start_time
    if duration:
        appt.duration = duration

    appt.status = Appointments.Status.CONFIRMED
    appt.calendar_api_id = calendly_event_uri

    appt.calendly_event_name = event.get("name")
    appt.calendly_event_status = event.get("status", "active")
    appt.calendly_created_at = parse_datetime(event.get("created_at")) if event.get("created_at") else None
    appt.calendly_updated_at = parse_datetime(event.get("updated_at")) if event.get("updated_at") else None

    location = event.get("location", {}) or {}
    appt.calendly_location_type = location.get("type")
    appt.calendly_join_url = location.get("join_url")
    appt.calendly_organization_uri = event.get("organization")
    appt.calendly_host_email = host_email

    appt.save()

    # ---- Create Invitee ----
    invitee_uri = invitee.get("uri")
    Invitee.objects.get_or_create(
        calendly_invitee_uri=invitee_uri,
        defaults={
            "appointment": appt,
            "name": invitee.get("name", ""),
            "email": invitee.get("email", ""),
            "phone_number": invitee.get("text_reminder_number"),
            "status": invitee.get("status", "active"),
            "canceled": invitee.get("canceled", False),
            "cancellation_reason": invitee.get("cancellation_reason"),
            "reschedule_url": invitee.get("reschedule_url"),
            "calendly_created_at": parse_datetime(invitee.get("created_at")) if invitee.get("created_at") else None,
            "calendly_updated_at": parse_datetime(invitee.get("updated_at")) if invitee.get("updated_at") else None,
        },
    )

    return JsonResponse({"status": "ok"})
