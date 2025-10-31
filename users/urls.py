from django.urls import include, path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("signuppage/", views.signup_page, name="signuppage"),
    path("signup/", views.signup, name="signup"),
    path("confirmation-page/", views.confirmation_page, name="confirmation_page"),
    path("client/dashboard", views.client_dashboard, name="client_dashboard"),
    path("accounts/", include("allauth.urls")),
]
