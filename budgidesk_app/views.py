###################
# librerias
#################


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt

from .forms import CustomUserCreationForm
from .models import FiscalProfile

from logic.plan_tiers import require_plan
from logic.debugger import debug, check_template_exists

from logic.fill_pdf import generate_invoice_pdf
from django.http import FileResponse

# librerias para stripe
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json

from logic import stripe as stripe_logic


######################################
def login_view(request):
    debug("Accessing login_view")
    check_template_exists("budgidesk_app/login.html")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            debug("User authenticated successfully")
            return redirect("dashboard")
        else:
            debug("Authentication failed")
            return render(request, "budgidesk_app/login.html", {"error": "Invalid username or password"})
    return render(request, "budgidesk_app/login.html")


def register_view(request):
    debug("Accessing register_view")
    check_template_exists("budgidesk_app/register.html")
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            debug("User registered successfully")
            login(request, user)
            return redirect('onboarding')
        else:
            debug("Registration form invalid")
    else:
        form = CustomUserCreationForm()
    return render(request, 'budgidesk_app/register.html', {'form': form})


@login_required
def invoice_create_view(request):
    try:
        profile = FiscalProfile.objects.get(user=request.user)
    except FiscalProfile.DoesNotExist:
        return redirect('onboarding')

    if request.method == 'POST':
        profile.invoice_count += 1
        profile.save()

        if request.user.plan == 'lite' and profile.invoice_count > 5:
            return redirect('pricing')

        return render(request, "budgidesk_app/dash/invoice/invoice_created.html", {
            'profile': profile
        })

    return render(request, "budgidesk_app/dash/invoice/invoice_create.html", {
        'invoice_count': profile.invoice_count
    })
 


@require_plan('smart')
@login_required
def invoice_list_view(request):
    debug("Accessing invoice_list_view")
    check_template_exists("budgidesk_app/invoices/invoice_list.html")
    return render(request, "budgidesk_app/invoices/invoice_list.html")


@require_plan('smart')
@login_required
def tax_report_view(request):
    debug("Accessing tax_report_view")
    check_template_exists("budgidesk_app/taxes/tax_report.html")
    return render(request, "budgidesk_app/taxes/tax_report.html")


@require_plan('smart')
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


@require_plan('elite')
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
    if request.method == "POST":
        FiscalProfile.objects.create(
            user=request.user,
            full_name=request.POST.get("full_name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            business_name=request.POST.get("business_name"),
            currency=request.POST.get("currency"),
            vat_registered=('vat_registered' in request.POST),
            vat_number=request.POST.get("vat_number", ''),
            pps_number=request.POST.get("pps_number", ''),
            iban=request.POST.get("iban", ''),
            logo=request.FILES.get("logo"),
        )
        debug(f"FiscalProfile created for {request.user.username}")
        return redirect("dashboard")
    return render(request, "budgidesk_app/onboard.html")


def checkout_view(request):
    debug("Accessing checkout_view")
    plan = request.GET.get('plan', 'smart_monthly')
    plan_options = {
        'smart_monthly': {'name': 'Budsi Smart', 'amount': 9, 'interval': 'month'},
        'elite_monthly': {'name': 'Budsi Elite', 'amount': 12, 'interval': 'month'},
        'smart_annual': {'name': 'Budsi Smart (Annual)', 'amount': 90, 'interval': 'year'},
        'elite_annual': {'name': 'Budsi Elite (Annual)', 'amount': 120, 'interval': 'year'},
    }
    if plan not in plan_options:
        plan = 'smart_monthly'
    details = plan_options[plan]
    details['plan_code'] = plan
    return render(request, 'budgidesk_app/payment.html', details)


@csrf_exempt
@login_required
def process_payment_view(request):
    debug("Accessing process_payment_view")
    if request.method == "POST":
        plan_code = request.GET.get("plan", "smart_monthly")
        user = request.user
        if "elite" in plan_code:
            user.plan = "elite"
        elif "smart" in plan_code:
            user.plan = "smart"
        else:
            user.plan = "lite"
        user.save()
        debug(f"Plan actualizado para {user.username}: {user.plan}")
        return redirect("dashboard")
    return redirect("checkout")


@login_required
def pricing_view(request):
    debug("Accessing pricing_view")
    check_template_exists("budgidesk_app/pricing.html")
    return render(request, "budgidesk_app/pricing.html")


@login_required
def dashboard_view(request):
    debug("Accessing dashboard_view")
    check_template_exists("budgidesk_app/dashboard.html")
    return render(request, "budgidesk_app/dashboard.html")


# 🔽 Nuevas vistas para las secciones movidas al subdirectorio "dash"

@login_required
def flow_view(request):
    return render(request, "budgidesk_app/dash/flow/flow.html")

@login_required
def pulse_view(request):
    return render(request, "budgidesk_app/dash/pulse/pulse.html")

@login_required
def buzz_view(request):
    return render(request, "budgidesk_app/dash/buzz/buzz.html")

@login_required
def track_view(request):
    return render(request, "budgidesk_app/dash/track/track.html")

@login_required
def tax_view(request):
    return render(request, "budgidesk_app/dash/tax/tax_report.html")

@login_required
def doc_view(request):
    return render(request, "budgidesk_app/dash/doc/legal_templates.html")

@login_required
def nest_view(request):
    return render(request, "budgidesk_app/dash/nest/nest.html")

@login_required
def whiz_view(request):
    return render(request, "budgidesk_app/dash/whiz/whiz.html")

@login_required
def help_view(request):
    return render(request, "budgidesk_app/dash/help_support/support.html")


@login_required
def create_invoice_pdf_view(request):
    profile = FiscalProfile.objects.get(user=request.user)
    pdf_path = generate_invoice_pdf(profile)
    return FileResponse(open(pdf_path, 'rb'), as_attachment=True, filename="invoice.pdf")

# Funciones para los pago tipo stripe     


@csrf_exempt
def create_payment_intent_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        amount = data.get("amount", 1000)  # 10.00 euros, en centavos
        intent = stripe_logic.create_payment_intent(amount)
        return JsonResponse({"clientSecret": intent.client_secret})
    return JsonResponse({"error": "Método no permitido"}, status=405)

@login_required
def payment_page(request):
    debug("Accessing checkout_view")  # puedes actualizar el texto si quieres
    plan = request.GET.get('plan', 'smart_monthly')
    plan_options = {
        'smart_monthly': {'name': 'Budsi Smart', 'amount': 9, 'interval': 'mes'},
        'elite_monthly': {'name': 'Budsi Elite', 'amount': 12, 'interval': 'mes'},
        'smart_annual': {'name': 'Budsi Smart (Anual)', 'amount': 90, 'interval': 'año'},
        'elite_annual': {'name': 'Budsi Elite (Anual)', 'amount': 120, 'interval': 'año'},
    }
    if plan not in plan_options:
        plan = 'smart_monthly'
    details = plan_options[plan]
    details['plan_code'] = plan
    details['STRIPE_PUBLIC_KEY'] = settings.STRIPE_PUBLIC_KEY 
    return render(request, 'budgidesk_app/payment.html', details)