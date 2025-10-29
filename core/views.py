# views.py is responsible for defining how the app ( this file, views.py, is in the app "core") interacts with users' requests like for data processing, rendering pages, responding to actions
# essentialy: user interactions -> tangible responses

from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
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
def practice_areas(r):
    content = WebsiteContent.objects.latest('created_at')
    return render(r, "practice_areas.html", {"content": content})
def about(r): return render(r, "about.html")
def services(r): return render(r, "services.html")
def contact(r): return render(r, "contact.html")
def payment(r): return render(r, "payment.html")
def schedule(r): return render(r, "schedule.html")
# We should start to think about refactoring the views into separated views files and import them into this main views file.
def signup(r):
    User = get_user_model()
    if r.method == 'POST':
        # Get form data manually from signup.html form post request
        first_name = r.POST.get('first-name')
        last_name = r.POST.get('last-name')
        email = r.POST.get('email')
        phone_number = r.POST.get('phone-number')
        password1 = r.POST.get('password')
        password2 = r.POST.get('re-password')

        # Password Check (if password mismatch, return empty response).
        if password1 != password2:
            messages.error(r, "Passwords do not match.")
            return render(r, 'signup.html')
        # Checks if User Exists in Database (checks email, returns empty response).
        if User.objects.filter(email=email).exists():
            messages.error(r, "An account with that email already exists.")
            return render(r, 'signup.html')
        
        # Create User if Passes Validation.
        user = User.objects.create_user(
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number
        )

        # Create Email Address Object.
        email_address = EmailAddress.objects.create(
            user=user,
            email=user.email,
            primary=True,
            verified=False
        )

        # Create Email Confirmation using the model configured by allauth
        # (HMAC vs DB-backed). This ensures the generated key matches what
        # the confirmation view expects when validating the link.
        model = get_emailconfirmation_model()
        email_confirmation = model.create(email_address)
        # Only call save() if the returned object is a DB model instance
        # (HMAC-based confirmations won't have a save method).
        if hasattr(email_confirmation, "save"):
            email_confirmation.save()

        # Send Email Confirmation.
        email_confirmation.send(request=r, signup=True)

        return complete_signup(
            r,
            user,
            allauth_settings.EMAIL_VERIFICATION,
            success_url=reverse('client_dashboard')
        )
    return render(r, 'signup.html')
def email_verification_notice(r):
    return render(r, 'confirmation-page.html')
def confirmation_page(r):
    return render(r, 'confirmation-page.html')
def login(r): 
    role = r.GET.get("role", "guest")
    return render(r, "login.html", {"role": role})

# admin views (login temporarily disabled for testing)
# @login_required
def admin_dashboard(r): return render(r, "admin/dashboard.html")
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
# @login_required
def logout_view(r):
    from django.contrib.auth import logout
    logout(r)
    return render(r, "logout.html")

# Client Views
#@login_required
def client_about(r): return render(r, "client/about.html")
#@login_required
def client_account(r): return render(r, "client/account.html")
#@login_required
def client_dashboard(r): return render(r, "client/dashboard.html")
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