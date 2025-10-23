# urls.py maps URLs to views

from django.urls import path
from . import views

urlpatterns = [
    # Public pages
    path("", views.home, name="home"),
    path("practice-areas/", views.practice_areas, name="practice-areas"),
    path("about/", views.about, name="about"),
    path("services/", views.services, name="services"),
    path("contact/", views.contact, name="contact"),
    path("payment/", views.payment, name="payment"),
    path("schedule/", views.schedule, name="schedule"),
    path("login/", views.login, name="login"),
    path("signup/", views.signup, name="signup"),

    # admin panel pages (using 'dashboard' prefix to avoid conflict with django admin)
    path("administrator/dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("administrator/dashboard/schedule/", views.admin_schedule, name="admin_schedule"),
    path("administrator/dashboard/transactions/", views.admin_transactions, name="admin_transactions"),
    path("administrator/dashboard/clients/", views.admin_clients, name="admin_clients"),
    path("administrator/dashboard/editor/", views.admin_editor, name="admin_editor"),
    path("administrator/dashboard/history/", views.admin_history, name="admin_history"),
    path("administrator/logout/", views.logout_view, name="logout"),

    # client pages 
    path("client/about/", views.client_about, name="client_about"),
    path("client/account/", views.client_account, name="client_account"),
    path("client/contact/", views.client_contact, name="client_contact"),
    path("client/dashboard/", views.client_dashboard, name="client_dashboard"),
    path("client/payment/", views.client_payment, name="client_payment"),
    path("client/practice-areas/", views.client_practice_areas, name="client_practice_areas"),
    path("client/schedule/", views.client_schedule, name="client_schedule"),
    path("client/transactions/", views.client_transactions, name="client_transactions"),

    # I have these paths below commented out because when we implement authentication, users will be authenticated with the auth_views method

    #path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    # path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    # path("password-reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
]
