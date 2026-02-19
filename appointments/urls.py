from django.urls import path
from . import views

urlpatterns = [
    path("webhooks/calendly/", views.calendly_webhook, name="calendly_webhook"),
    path("calendly/oauth/start/", views.calendly_oauth_start, name="calendly_oauth_start"),
    path("calendly/oauth/callback/", views.calendly_oauth_callback, name="calendly_oauth_callback"),
]
