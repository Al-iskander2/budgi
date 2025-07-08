from django.urls import path
from django.shortcuts import redirect
from django.contrib.auth.views import LogoutView
from .views import (
    login_view,
    register_view,
    dashboard_view,
    invoice_create_view,
    invoice_list_view,
    tax_report_view,
    balance_overview_view,
    account_settings_view,
    legal_templates_view,
    reminders_view,
    intro_view,           # nuevo
    onboarding_view       # nuevo
)

urlpatterns = [
    # Página principal (landing animada)
    path("", intro_view, name="intro"),

    # Autenticación
    path("login/", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),

    # Dashboard principal
    path("dashboard/", dashboard_view, name="dashboard"),

    # Onboarding fiscal paso a paso
    path("onboarding/", onboarding_view, name="onboarding"),

    # Facturación
    path("invoice/create/", invoice_create_view, name="invoice_create"),
    path("invoice/list/", invoice_list_view, name="invoice_list"),

    # Impuestos
    path("tax/report/", tax_report_view, name="tax_report"),

    # Finanzas
    path("finances/overview/", balance_overview_view, name="balance_overview"),

    # Extras
    path("account/settings/", account_settings_view, name="account_settings"),
    path("legal/templates/", legal_templates_view, name="legal_templates"),
    path("reminders/", reminders_view, name="reminders"),
]
