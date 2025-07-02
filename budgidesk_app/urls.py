from django.urls import path
from django.shortcuts import redirect
from .views import login_view, dashboard_view, register_view  # 👈 importa las vistas

urlpatterns = [
    path("", lambda request: redirect("login")),
    path("login/", login_view, name="login"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("register/", register_view, name="register"),
]
