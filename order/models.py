from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BillingInfo(models.Model):
    billing_key = models.CharField(primary_key=True, unique=True, max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
