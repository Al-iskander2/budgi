# budgidesk_project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("budgidesk_app.urls")),  # 👈 conecta todas las rutas de tu app
]
