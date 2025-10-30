from allauth.account.adapter import DefaultAccountAdapter
from django.shortcuts import redirect

class MyAccountAdapter(DefaultAccountAdapter):
    def respond_user_inactive(self, request, user):
        return redirect('confirmation_page')

    def confirm_email(self, request, email_address):
        """
        Called when an email address is confirmed. Ensures the related user
        account is activated (is_active=True) after successful confirmation.
        """
        result = super().confirm_email(request, email_address)
        try:
            user = email_address.user
            if result and not user.is_active:
                user.is_active = True
                user.save()
        except Exception:
            # Handle exception here? Optional for now...
            pass
        return result