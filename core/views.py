# views.py is responsible for defining how the app ( this file, views.py, is in the app "core") interacts with users' requests like for data processing, rendering pages, responding to actions
# essentialy: user interactions -> tangible responses

from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required

# Public views
def home(r): return render(r, "home.html")
def practice_areas(r): return render(r, "practice-areas.html")
def about(r): return render(r, "about.html")
def services(r): return render(r, "services.html")
def contact(r): return render(r, "contact.html")
def payment(r): return render(r, "payment.html")
def schedule(r): return render(r, "schedule.html")
def login(r): return render(r, "login.html")



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