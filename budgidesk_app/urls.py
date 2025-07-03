from django.urls import path
from django.shortcuts import redirect
from .views import (
    login_view,
    dashboard_view,
    register_view,
    invoice_create_view,
    tax_report_view,  # si también lo usas
)


urlpatterns = [
    path("", lambda request: redirect("login")),
    path("login/", login_view, name="login"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("register/", register_view, name="register"),
    path("invoice/create/", invoice_create_view, name="invoice_create"),  # 
    path("tax/report/", tax_report_view, name="tax_report"),              # 
]