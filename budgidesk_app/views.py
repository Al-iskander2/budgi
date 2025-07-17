from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from logic.plan_tiers import require_plan
from django.views.decorators.csrf import csrf_exempt






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

    #  Verificar si el usuario ya tiene un perfil fiscal
    from .models import FiscalProfile
    try:
        FiscalProfile.objects.get(user=request.user)
    except FiscalProfile.DoesNotExist:
        return redirect("onboarding")  #  si no hay perfil, va al onboarding

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


def checkout_view(request):
    plan = request.GET.get('plan', 'smart_monthly')

    plan_options = {
        'smart_monthly': {
            'name': 'Budsi Smart',
            'amount': 9,
            'interval': 'month',
        },
        'elite_monthly': {
            'name': 'Budsi Elite',
            'amount': 12,
            'interval': 'month',
        },
        'smart_annual': {
            'name': 'Budsi Smart (Annual)',
            'amount': 90,
            'interval': 'year',
        },
        'elite_annual': {
            'name': 'Budsi Elite (Annual)',
            'amount': 120,
            'interval': 'year',
        }
    }

    if plan not in plan_options:
        plan = 'smart_monthly'

    plan_details = plan_options[plan]
    plan_details['plan_code'] = plan

    return render(request, 'budgidesk_app/payment.html', plan_details)

@csrf_exempt
@login_required
def process_payment_view(request):
    debug("Accessing process_payment_view")

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        card_number = request.POST.get("card_number")
        exp_month = request.POST.get("exp_month")
        cvc = request.POST.get("cvc")
        plan_code = request.GET.get("plan", "smart_monthly")

        debug(f"Submitted payment for plan: {plan_code} by {name}")

        # En producción deberías integrar Stripe u otra pasarela aquí.

        # Guardar el plan en el usuario
        user = request.user
        if "elite" in plan_code:
            user.plan = "elite"
        elif "smart" in plan_code:
            user.plan = "smart"
        else:
            user.plan = "lite"

        user.save()
        debug(f" Plan actualizado: {user.plan}")

        return redirect("dashboard")

    return redirect("checkout")  # fallback si no es POST