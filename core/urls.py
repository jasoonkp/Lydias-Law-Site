# urls.py maps URLs to views

from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("services/", views.services, name="services"),
    path("contact/", views.contact, name="contact"),
    path("schedule/", views.schedule, name="schedule"),
    path("login/", views.login, name="login"),


    # I have these paths below commented out because when we implement authentication, users will be authenticated with the auth_views method

    #path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    # path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    # path("password-reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
]
