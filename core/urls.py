# urls.py maps URLs to views

from django.urls import path, include
from . import views
from sitecontent.views import about
from sitecontent.views import home
from sitecontent.views import contact

urlpatterns = [
    # Public pages
    path("", home, name="home"),
    path("practice-areas/", views.practice_areas, name="practice_areas"),
    path("about/", about, name="about"),
    path("services/", views.services, name="services"),
    path("contact/", contact, name="contact"),
    path("payment/", views.payment, name="payment"),
    path("schedule/", views.schedule, name="schedule"),
    path("login/", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("accounts/", include("allauth.urls")),
    path('verify/', views.confirmation_page, name='confirmation_page'),
    path("confirmation-page/", views.confirmation_page, name="confirmation_page"),

    # admin panel pages (using 'administrator' to avoid conflict with django "admin" keyword)
    path("administrator/", views.admin_dashboard, name="admin_dashboard"),
    path("administrator/dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("administrator/schedule/", views.admin_schedule, name="admin_schedule"),
    path("administrator/transactions/", views.admin_transactions, name="admin_transactions"),
    path("administrator/clients/", views.admin_clients, name="admin_clients"),
    path("administrator/editor/", views.admin_editor, name="admin_editor"),
    path("administrator/history/", views.admin_history, name="admin_history"),
    path("administrator/logout/", views.logout_view, name="logout"),

    # client pages 
    path("client/about/", about, {'client': True}, name="client_about"),
    path("client/account/", views.client_account, name="client_account"),
    path("client/contact/", contact, {'client': True}, name="client_contact"),
    path("client/dashboard/", views.client_dashboard, name="client_dashboard"),
    path("client/payment/", views.client_payment, name="client_payment"),
    path("client/practice-areas/", views.client_practice_areas, name="client_practice_areas"),
    path("client/schedule/", views.client_schedule, name="client_schedule"),
    path("client/transactions/", views.client_transactions, name="client_transactions"),
    path("client/appointment_request_confirmation/", views.client_appointment_request_confirmation, name="client_appointment_request_confirmation"),
    path("client/appointment_denied_confirmation/", views.client_appointment_denied_confirmation, name="client_appointment_denied_confirmation"),
    path("client/appointment_approved_confirmation/", views.client_appointment_approved_confirmation, name="client_appointment_approved_confirmation"),

    # I have these paths below commented out because when we implement authentication, users will be authenticated with the auth_views method

    #path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    # path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    # path("password-reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),


]
