from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model, login as auth_login, authenticate
from allauth.account.utils import complete_signup
from allauth.account import app_settings as allauth_settings
from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress, EmailConfirmation, get_emailconfirmation_model
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

# Directs to login page
def login(r): 
    role = r.GET.get("role", "guest")
    return render(r, "users/login.html", {"role": role})

# Handles login form submission and authenticates user
@require_http_methods(["GET", "POST"])
def login_view(request):
    """
    Render login page (GET) and authenticate credentials (POST).
    Uses django.contrib.auth.authenticate() with email + password.
    """
    if request.method == "GET":
        role = request.GET.get("role", "guest")
        return render(request, "users/login.html", {"role": role})

    # POST
    email = (request.POST.get("email") or "").strip().lower()
    password = request.POST.get("password") or ""

    # authenticate() will look up by USERNAME_FIELD (email in our model)
    user = authenticate(request, email=email, password=password)

    if user is None:
        # Wrong email/password
        messages.error(request, "Invalid credentials.")
        return render(request, "users/login.html", {"role": request.GET.get("role", "guest")}, status=401)

    if not user.is_active:
        # Users have is_active=False until email is verified
        messages.error(request, "Please verify your email to activate your account.")
        return render(request, "users/login.html", {"role": request.GET.get("role", "guest")}, status=403)

    # Success: log them in and redirect
    auth_login(request, user)
    return redirect("client_dashboard")



def signup_page(r):
    return render(r, "users/signup.html")

# We should start to think about refactoring the views into separated views files and import them into this main views file.
# Signup view, directs to signup page and handles signup form submission
def signup(r):
    User = get_user_model()
    if r.method == 'POST':
        first_name = (r.POST.get('first-name') or "").strip()
        last_name = (r.POST.get('last-name') or "").strip()
        email = (r.POST.get('email') or "").strip()
        phone_number = (r.POST.get('phone-number') or "").strip()

        password1 = r.POST.get('password1') or ""
        password2 = r.POST.get('password2') or ""

        # Basic checks
        if password1 != password2:
            messages.error(r, "Passwords do not match.")
            return render(r, 'users/signup.html')

        if password1 != password1.strip():
            messages.error(r, "Password cannot start or end with spaces.")
            return render(r, 'users/signup.html')

        if User.objects.filter(email__iexact=email).exists():
            messages.error(r, "An account with that email already exists.")
            return render(r, 'users/signup.html')

        # Create the user with a **real** password
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

# Email verification notice view
def email_verification_notice(r):
    return render(r, 'users/confirmation-page.html')

# Email confirmation page view
def confirmation_page(r):
    return render(r, 'users/confirmation-page.html')