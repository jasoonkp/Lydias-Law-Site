from django.shortcuts import render
from django.conf import settings
from django.db import transation
import stripe

# Create your views here.
def get_or_create_stripe_customer_id(user):
    stripe.api_key = settings.STRIPE_API_KEY

    # locks the user's row to prevent duplicate stripe customers for one user
    with transaction.atomic():
        user = type(user).objects.select_for_update().get(pk=user.pk)

    # check if client has stripe customer id
    if user.provider_customer_id:
        return user.provider_customer_id
    
    # create Stripe customer id if it doesn't exist
    customer = stripe.Customer.create(
        email=user.email,
        name=f"{user.first_name} {user.last_name}",
        metadata={"user_id": str(user.id)},
    )

    # save Stripe customer id
    user.provider_customer_id = customer.id
    user.save()

    return customer.id
    