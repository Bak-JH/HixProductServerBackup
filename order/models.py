from product.models import ProductSerial
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

# Create your models here.
class BillingInfo(models.Model):
    billing_key = models.CharField(primary_key=True, unique=True, max_length=50)
    card_name = models.CharField(max_length=50, default="")
    card_number = models.PositiveSmallIntegerField(default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)

class PaymentHistory(models.Model):
    receipt_id = models.CharField(primary_key=True, unique=True, max_length=100)
    receipt_url = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    serial = models.ForeignKey('product.ProductSerial', on_delete=models.SET_NULL, null=True, blank=True)
    billing_info = models.ForeignKey('order.BillingInfo', on_delete=models.SET_NULL, null=True, blank=True, db_constraint=False)
    refunded = models.BooleanField(default=False)

class PricingPolicy(models.Model):
    ONESHOT = 'ONE'
    PERIOD = 'PER'
    PurchaseMethod = [
        (ONESHOT, 'OneShot'),
        (PERIOD, 'Period')
    ]
    pricing_id = models.UUIDField(default=uuid.uuid4)
    method = models.CharField(max_length=10, choices=PurchaseMethod, default=ONESHOT)
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    price = models.FloatField()