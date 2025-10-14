# views.py is responsible for defining how the app ( this file, views.py, is in the app "core") interacts with users' requests like for data processing, rendering pages, responding to actions
# essentialy: user interactions -> tangible responses

from django.shortcuts import render, HttpResponse

# Create your views here.
def home(r): return render(r, "home.html")
def about(r): return render(r, "about.html")
def services(r): return render(r, "services.html")
def contact(r): return render(r, "contact.html")
def schedule(r): return render(r, "schedule.html")
def login(r): return render(r, "login.html")