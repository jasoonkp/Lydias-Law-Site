import json
import logging

from django.conf import settings
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import stripe

from .models import Invoice, StripeWebhookEvent

# Standard Django logger for recording webhook activity.
logger = logging.getLogger(__name__)


@csrf_exempt
def stripe_webhook(request):
    """
    Stripe sends server-to-server webhook events to this endpoint.
    We verify the Stripe signature, de-duplicate events, and update
    invoice status based on the event type.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    # The shared secret from Stripe's dashboard, used to verify the signature.
    webhook_secret = getattr(settings, "STRIPE_WEBHOOK_SECRET", "")
    if not webhook_secret:
        logger.error("Stripe webhook secret not configured.")
        return JsonResponse({"error": "Webhook not configured"}, status=500)

    # Stripe requires the raw request body for signature verification.
    payload = request.body
    sig_header = request.headers.get("Stripe-Signature")
    if not sig_header:
        logger.warning("Missing Stripe-Signature header.")
        return JsonResponse({"error": "Missing signature"}, status=400)

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except ValueError:
        logger.warning("Invalid Stripe webhook payload.")
        return JsonResponse({"error": "Invalid payload"}, status=400)
    except stripe.error.SignatureVerificationError:
        logger.warning("Invalid Stripe webhook signature.")
        return JsonResponse({"error": "Invalid signature"}, status=400)

    # Store the raw JSON payload (signature already verified above).
    event_data = json.loads(payload.decode("utf-8"))
    event_id = event_data.get("id")
    if not event_id:
        logger.warning("Stripe webhook missing event id.")
        return JsonResponse({"error": "Missing event id"}, status=400)

    try:
        with transaction.atomic():
            # Store the event so duplicates can be detected safely.
            webhook_event, created = StripeWebhookEvent.objects.get_or_create(
                event_id=event_id,
                defaults={
                    "event_type": event_data.get("type", ""),
                    "payload": event_data,
                },
            )
    except IntegrityError:
        created = False
        webhook_event = None

    if not created:
        logger.info(
            "Duplicate Stripe event received: %s",
            event_id,
        )
        return JsonResponse({"status": "duplicate"}, status=200)

    event_type = event_data.get("type")
    invoice_obj = event_data.get("data", {}).get("object", {})

    if event_type in {"invoice.paid", "invoice.payment_failed"}:
        # Stripe invoice metadata can include our local invoice ID.
        metadata = invoice_obj.get("metadata") or {}
        local_invoice_id = metadata.get("local_invoice_id") or metadata.get("invoice_id")
        stripe_invoice_id = invoice_obj.get("id")

        invoice = None
        # Prefer a direct local ID lookup when available.
        if local_invoice_id:
            invoice = Invoice.objects.filter(id=local_invoice_id).first()
        # Fall back to the Stripe invoice ID if stored in our database.
        if not invoice and stripe_invoice_id:
            invoice = Invoice.objects.filter(stripe_invoice_id=stripe_invoice_id).first()

        if not invoice:
            logger.warning(
                "Stripe invoice event received but no matching invoice found. "
                "event_id=%s stripe_invoice_id=%s local_invoice_id=%s",
                event_id,
                stripe_invoice_id,
                local_invoice_id,
            )
            return JsonResponse({"status": "ignored"}, status=200)

        if event_type == "invoice.paid":
            # Paid means the invoice is complete.
            invoice.status = Invoice.Status.PAID
            invoice.paid = True
        elif event_type == "invoice.payment_failed":
            # Payment failed means the invoice is still unpaid.
            invoice.status = Invoice.Status.PAYMENT_FAILED
            invoice.paid = False

        invoice.save(update_fields=["status", "paid"])
        logger.info(
            "Stripe invoice updated. invoice_id=%s status=%s event_id=%s",
            invoice.id,
            invoice.status,
            event_id,
        )

    logger.info(
        "Stripe webhook processed. event_id=%s type=%s",
        event_id,
        event_type,
    )
    return JsonResponse({"status": "success"}, status=200)
