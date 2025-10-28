from django.shortcuts import render
from .models import WebsiteContent
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
def about(request):
    try:
        # Attempt to get the latest content
        content = WebsiteContent.objects.order_by('-versionNumber').first()

        if not content:
            # Fallback if no content exists
            content = WebsiteContent(
                nameTitle="No Content Available",
                aboutMeDescription="No description available."
            )

        # Render the normal about page
        return render(request, 'about.html', {'content': content})

    except Exception as e:
        # Log the error
        print(f"ERROR in about view: {e}")

        # Error page
        return HttpResponseServerError("An error occurred while loading the About page.")




