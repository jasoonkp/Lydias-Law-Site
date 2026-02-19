from .models import WebsiteContent

"""
Context Processor to make website content available globally
Ensures the footer renders dynamically on every page
"""
def footer_content(request):
    try:
        content = WebsiteContent.objects.order_by('created_at').first()
    except Exception:
        content = None
        
    return{"content": content}