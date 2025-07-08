from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login




# Herramientas de depuración
from logic.debugger import debug, check_template_exists


def login_view(request):
    debug("Accessing login_view")
    check_template_exists("budgidesk_app/login.html")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # 👈 inicia sesión
            debug("User authenticated successfully")
            return redirect("dashboard")
        else:
            debug("Authentication failed")
            return render(request, "budgidesk_app/login.html", {
                "error": "Invalid username or password"
            })

    return render(request, "budgidesk_app/login.html")


def register_view(request):
    debug("Accessing register_view")
    check_template_exists("budgidesk_app/register.html")

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            debug("User registered successfully")
            return redirect('login')
        else:
            debug("Registration form invalid")
    else:
        form = UserCreationForm()

    return render(request, 'budgidesk_app/register.html', {'form': form})


@login_required
def dashboard_view(request):
    debug("Accessing dashboard_view")
    check_template_exists("budgidesk_app/dashboard.html")
    return render(request, "budgidesk_app/dashboard.html")


@login_required
def invoice_create_view(request):
    debug("Accessing invoice_create_view")
    check_template_exists("budgidesk_app/invoices/invoice_create.html")
    return render(request, "budgidesk_app/invoices/invoice_create.html")


@login_required
def invoice_list_view(request):
    debug("Accessing invoice_list_view")
    check_template_exists("budgidesk_app/invoices/invoice_list.html")
    return render(request, "budgidesk_app/invoices/invoice_list.html")


@login_required
def tax_report_view(request):
    debug("Accessing tax_report_view")
    check_template_exists("budgidesk_app/taxes/tax_report.html")
    return render(request, "budgidesk_app/taxes/tax_report.html")


@login_required
def balance_overview_view(request):
    debug("Accessing balance_overview_view")
    check_template_exists("budgidesk_app/finances/balance_overview.html")
    return render(request, "budgidesk_app/finances/balance_overview.html")


@login_required
def account_settings_view(request):
    debug("Accessing account_settings_view")
    check_template_exists("budgidesk_app/account_settings.html")
    return render(request, "budgidesk_app/account_settings.html")


@login_required
def legal_templates_view(request):
    debug("Accessing legal_templates_view")
    check_template_exists("budgidesk_app/legal_templates.html")
    return render(request, "budgidesk_app/legal_templates.html")


@login_required
def reminders_view(request):
    debug("Accessing reminders_view")
    check_template_exists("budgidesk_app/reminders.html")
    return render(request, "budgidesk_app/reminders.html")

def intro_view(request):
    debug("Accessing intro_view")
    check_template_exists("budgidesk_app/intro.html")
    return render(request, "budgidesk_app/intro.html")

@login_required
def onboarding_view(request):
    debug("Accessing onboarding_view")
    check_template_exists("budgidesk_app/onboard.html")
    return render(request, "budgidesk_app/onboard.html")


def register_view(request):
    debug("Accessing register_view")
    check_template_exists("budgidesk_app/register.html")

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 👈 iniciar sesión automáticamente
            return redirect('onboarding')  # 👈 redirige al onboarding
        else:
            debug("Registration form invalid")
    else:
        form = UserCreationForm()

    return render(request, 'budgidesk_app/register.html', {'form': form})


from .models import FiscalProfile

@login_required
def onboarding_view(request):
    debug("Accessing onboarding_view")
    check_template_exists("budgidesk_app/onboard.html")

    if request.method == "POST":
        FiscalProfile.objects.create(
            user=request.user,
            full_name=request.POST.get("full_name"),
            pps_number=request.POST.get("pps_number"),
            birthdate=request.POST.get("birthdate"),
            income=request.POST.get("income"),
            business_type=request.POST.get("business_type"),
        )
        return redirect("dashboard")

    return render(request, "budgidesk_app/onboard.html")


