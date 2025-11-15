from django.urls import path
from . import views

urlpatterns = [
    path("webhooks/calendly/", views.calendly_webhook, name="calendly_webhook"),
]
