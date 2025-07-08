

from django.db import models
from django.contrib.auth.models import User

class FiscalProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    pps_number = models.CharField(max_length=20)
    birthdate = models.DateField()
    income = models.DecimalField(max_digits=10, decimal_places=2)
    business_type = models.CharField(max_length=100)

    def __str__(self):
        return f"Fiscal data of {self.user.username}"
