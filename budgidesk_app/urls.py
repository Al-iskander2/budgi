from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path("", views.intro_view, name="intro"),

    # Autenticación
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),

    # Dashboard principal
    path("dashboard/", views.dashboard_view, name="dashboard"),

    # Onboarding
    path("onboarding/", views.onboarding_view, name="onboarding"),

    # Facturación
    path("invoice/create/", views.invoice_create_view, name="invoice_create"),
    path("invoice/list/", views.invoice_list_view, name="invoice_list"),

    # Impuestos
    path("tax/report/", views.tax_report_view, name="tax_report"),

    # Finanzas
    path("finances/overview/", views.balance_overview_view, name="balance_overview"),

    # Extras
    path("account/settings/", views.account_settings_view, name="account_settings"),
    path("legal/templates/", views.legal_templates_view, name="legal_templates"),
    path("reminders/", views.reminders_view, name="reminders"),

    # Pagos
    path("checkout/", views.checkout_view, name="checkout"),
    path("process-payment/", views.process_payment_view, name="process_payment"),

    # Precios / Upgrade
    path("pricing/", views.pricing_view, name="pricing"),
]
