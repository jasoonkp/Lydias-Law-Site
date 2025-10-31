# views.py is responsible for defining how the app ( this file, views.py, is in the app "core") interacts with users' requests like for data processing, rendering pages, responding to actions
# essentialy: user interactions -> tangible responses

from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model, logout
from allauth.account.utils import complete_signup
from allauth.account import app_settings as allauth_settings
from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress, EmailConfirmation, get_emailconfirmation_model
from django.views.decorators.csrf import csrf_exempt
from sitecontent.models import WebsiteContent


# Public views
def home(r):
    role = r.GET.get("role", "guest")
    return render(r, "home.html", {"role": role})
  
# Is this method 
def practice_areas(r):
    content = WebsiteContent.objects.latest('created_at')
    return render(r, "practice_areas.html", {"content": content})

def about(r): return render(r, "about.html")
def services(r): return render(r, "services.html")
def contact(r): return render(r, "contact.html")
def payment(r): return render(r, "payment.html")
def schedule(r): return render(r, "schedule.html")

def login(r): 
    role = r.GET.get("role", "guest")
    return render(r, "users/login.html", {"role": role})

# admin views (login temporarily disabled for testing)
# @login_required
# def admin_dashboard(r): return render(r, "admin/dashboard.html")
# @login_required
def admin_schedule(r): return render(r, "admin/schedule.html")
# @login_required
def admin_transactions(r): return render(r, "admin/transactions.html")
# @login_required
def admin_clients(r): return render(r, "admin/clients.html")
# @login_required
def admin_editor(r): return render(r, "admin/editor.html")
# @login_required
def admin_history(r): return render(r, "admin/history.html")

# Client Views
#@login_required
def client_about(r): return render(r, "client/about.html")
#@login_required
def client_account(r): return render(r, "client/account.html")
#@login_required
def client_contact(r): return render(r, "client/contact.html")
#@login_required
def client_payment(r): return render(r, "client/payment.html")
#@login_required
def client_practice_areas(r): return render(r, "client/practice_areas.html")
#@login_required
def client_schedule(r): return render(r, "client/schedule.html")
#@login_required
def client_transactions(r): return render(r, "client/transactions.html")
#@login_required
def client_appointment_request_confirmation(r): return render(r, "client/appointment_request_confirmation.html")
#@login_required
def client_appointment_denied_confirmation(r): return render(r, "client/appointment_denied_confirmation.html")
#@login_required
def client_appointment_approved_confirmation(r): return render(r, "client/appointment_approved_confirmation.html")