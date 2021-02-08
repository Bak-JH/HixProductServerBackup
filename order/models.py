from product.models import ProductSerial
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class BillingInfo(models.Model):
    billing_key = models.CharField(primary_key=True, unique=True, max_length=50)
    card_name = models.CharField(max_length=50, default="")
    card_number = models.PositiveSmallIntegerField(default=0)

class PaymentHistory(models.Model):
    receipt_id = models.CharField(primary_key=True, unique=True, max_length=100)
    receipt_url = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    serial = models.ForeignKey('product.ProductSerial', on_delete=models.SET_NULL, null=True)

class PricingPolicy(models.Model):
    ONESHOT = 'ONE'
    PERIOD = 'PER'
    PurchaseMethod = [
        (ONESHOT, 'OneShot'),
        (PERIOD, 'Period')
    ]
    method = models.CharField(max_length=10, choices=PurchaseMethod, default=ONESHOT)
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    price = models.FloatField()