from django.shortcuts import render
from .models import WebsiteContent
from django.contrib.auth import get_user_model
from django.http import HttpResponseServerError

# Create your views here.

# Home Page request
def home(request):
    try:
        # Attempt to get the latest content
        content = WebsiteContent.objects.order_by('-versionNumber').first()

        if not content:
            # Fallback if no content exists
            content = WebsiteContent(
                frontPageHeader="No Content Available",
                frontPageDescription="No description available."
            )

        # Render the normal about page
        return render(request, 'home.html', {'content': content})

    except Exception as e:
        # Log the error
        print(f"ERROR in about view: {e}")

        # Error page
        return HttpResponseServerError("An error occurred while loading the Home page.")


# About Page Request
def about(request, client=False):
    try:
        # Attempt to get the latest content from the WebsiteContent table
        content = WebsiteContent.objects.order_by('-versionNumber').first()

        # Fallback if no content exists
        if not content:
            
            content = WebsiteContent(
                nameTitle = "No Content Available",
                aboutMeDescription = "No description available."
            )
        
        # Fallback if no title exists
        if content and not content.nameTitle:
            content.nameTitle = "No Content Availabe"

        # Fallback if no phone number exists
        if content and not content.aboutMeDescription:
            content.aboutMeDescription = "No Content Available"

        # Check which page to render
        page = 'about.html'
        if client:
            page = 'client/about.html'

        # Render the about page
        return render(request, page, {'content': content})

    except Exception as e:
        # Log the error
        print(f"ERROR in about view: {e}")

        # Error page
        return HttpResponseServerError("An error occurred while loading the About page.")
    

# Contact Page request
def contact(request, client=False):
    try:
        User = get_user_model()

        # Attempt to get the latest content from WebsiteContent table
        location = WebsiteContent.objects.order_by('-versionNumber').first()

        # Attempts to get Lydia's information from User table
        lydia = User.objects.filter(role=User.Role.ADMIN).first()

        # Fallback if no location exists
        if not location:
            location = WebsiteContent(
                officeLocation="No Content Available"
            )

        # Fallback if no email exists
        if lydia and not lydia.email:
            lydia.email = "No Content Available"

        # Fallback if no phone number exists
        if lydia and not lydia.phone_number:
            lydia.phone_number = "No Content Available"

        # Check which page to render
        page = 'contact.html'
        if client:
            page = 'client/contact.html'

        # Render contact page
        return render(request, page, {
            'location': location,
            'lydia': lydia
        })
    
    except Exception as e:
        # Log the error
        print(f"ERROR in about view: {e}")

        # Error page
        return HttpResponseServerError("An error occurred while loading the Contact page.")


