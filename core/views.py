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
from django.conf import settings

''' Are these needed anymore if site content is covering them?
    Home, About, and Contact are all being handled by site content views,
    making some of these and potentially more in the future obsolete.
'''
# Public views
def home(r):
    role = r.GET.get("role", "guest")
    return render(r, "home.html", {"role": role, "GOOGLE_MAPS_API_KEY": settings.GOOGLE_MAPS_API_KEY})
  
# Is this method 
def practice_areas(r):
    content = WebsiteContent.objects.latest('created_at')
    return render(r, "practice_areas.html", {"content": content})

def about(r): return render(r, "about.html")
def services(r): return render(r, "services.html")
def contact(r): return render(r, "contact.html", {"GOOGLE_MAPS_API_KEY": settings.GOOGLE_MAPS_API_KEY})
def payment(r): return render(r, "payment.html")
def schedule(r): return render(r, "schedule.html")
def privacy(r): return render(r, "privacy.html")
def appointment_confirmation(r): return render (r, "appointment_confirmation.html")

def login(r): 
    role = r.GET.get("role", "guest")
    return render(r, "users/login.html", {"role": role})

# admin views (login temporarily disabled for testing)
# @login_required
#def admin_dashboard(r): return render(r, "admin/dashboard.html")
# @login_required
def admin_schedule(r): return render(r, "admin/schedule.html")
# @login_required
def admin_transactions(r): return render(r, "admin/transactions.html")
# @login_required
def admin_clients(r): return render(r, "admin/clients.html")
# @login_required
def admin_editor(request):
    """
    Admin editor view for editing WebsiteContent.
    Fetches the latest content version and allows editing.
    """
    from .forms import WebsiteContentForm

    # get the latest WebsiteContent or create default if none exists
    content = WebsiteContent.objects.order_by('-versionNumber').first()

    if content is None:
        content = WebsiteContent.objects.create(
            frontPageHeader="Welcome",
            frontPageDescription="Default description"
        )

    if request.method == 'POST':
        form = WebsiteContentForm(request.POST, instance=content)
        if form.is_valid():
            form.save()
            messages.success(request, 'Website content updated successfully!')
            return redirect('admin_editor')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = WebsiteContentForm(instance=content)

    return render(request, "admin/editor.html", {
        'form': form,
        'content': content,
    })
# @login_required
def admin_history(r): return render(r, "admin/history.html")
# @login_required
def admin_appointment_confirmation(r): return render(r, "admin/appointment_confirmation.html")
# @login_required
def admin_create_invoices(r): return render(r, "admin/create_invoice.html")

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
def client_practice_areas(r):
    content = WebsiteContent.objects.latest('created_at')
    return render(r, "client/practice_areas.html", {"content": content})
#@login_required
def client_schedule(r): return render(r, "client/schedule.html")
#@login_required
def client_transactions(r): return render(r, "client/transactions.html")
#@login_required
def client_privacy(r):
    return render(r, "client/privacy.html")
#@login_required
def client_appointment_request_confirmation(r): return render(r, "client/appointment_request_confirmation.html")
#@login_required
def client_appointment_denied_confirmation(r): return render(r, "client/appointment_denied_confirmation.html")
#@login_required
def client_appointment_confirmation(r): return render(r, "client/appointment_confirmation.html")
