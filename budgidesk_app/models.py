from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    plan = models.CharField(max_length=20, default='lite')  # lite, smart, elite

class FiscalProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=100)
    email = models.EmailField(default='')
    phone = models.CharField(max_length=20, blank=True)

    business_name = models.CharField(max_length=100)

    currency = models.CharField(
        max_length=3,
        choices=[('EUR','EUR'),('GBP','GBP'),('USD','USD')],
        default='EUR'
    )

    vat_registered = models.BooleanField(default=False)
    vat_number = models.CharField(max_length=20, blank=True)

    pps_number = models.CharField(max_length=20, blank=True)
    iban = models.CharField(max_length=34, blank=True)

    logo = models.ImageField(upload_to='user_logos/', blank=True, null=True)

    invoice_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Fiscal data of {self.user.username}"
