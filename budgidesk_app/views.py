from django.shortcuts import render, redirect

def login_view(request):
    if request.method == "POST":
        # lógica de autenticación opcional aquí
        return redirect("dashboard")
    return render(request, "budgidesk_app/login.html")

def dashboard_view(request):
    return render(request, "budgidesk_app/dashboard.html")
