from django.urls import path

from . import views

urlpatterns = [
    # Stripe webhook endpoint (server-to-server callbacks).
    path("webhooks/stripe/", views.stripe_webhook, name="stripe_webhook"),
]
