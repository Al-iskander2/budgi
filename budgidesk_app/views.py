from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

# Importa herramientas de depuración
from logic.debugger import debug, check_template_exists


def login_view(request):
    debug("🔑 Accessing login_view")
    check_template_exists("budgidesk_app/login.html")

    if request.method == "POST":
        # lógica de autenticación opcional aquí
        return redirect("dashboard")

    return render(request, "budgidesk_app/login.html")


def dashboard_view(request):
    debug("📊 Accessing dashboard_view")
    check_template_exists("budgidesk_app/dashboard.html")
    
    return render(request, "budgidesk_app/dashboard.html")


def register_view(request):
    debug("📝 Accessing register_view")
    check_template_exists("budgidesk_app/register.html")

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            debug("✅ User registered successfully")
            return redirect('login')  # redirige al login después de registrarse
        else:
            debug("❌ Registration form invalid")
    else:
        form = UserCreationForm()

    return render(request, 'budgidesk_app/register.html', {'form': form})
