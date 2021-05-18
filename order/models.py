from django.db.models.deletion import SET_NULL
from product.models import ProductSerial
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid
from django_celery_beat.models import PeriodicTask

# Create your models here.
class BillingInfo(models.Model):
    billing_key = models.CharField(primary_key=True, unique=True, max_length=50)
    card_name = models.CharField(max_length=50, default="")
    card_number = models.CharField(max_length=20, default="")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)

class PaymentHistory(models.Model):
    receipt_id = models.CharField(primary_key=True, unique=True, max_length=100)
    receipt_url = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    serial = models.ForeignKey('product.ProductSerial', on_delete=models.SET_NULL, null=True, blank=True)
    billing_info = models.ForeignKey('order.BillingInfo', on_delete=models.SET_NULL, null=True, blank=True, db_constraint=False)
    refunded = models.BooleanField(default=False)

class PricingPolicy(models.Model):
    ONEOFF = 'One-Off'
    MONTHLY = 'Monthly'
    YEARLY = 'Yearly'
    PurchaseMethod = [
        (ONEOFF, 'One-Off'),
        (MONTHLY, 'Monthly'),
        (YEARLY, 'Yearly')
    ]
    pricing_id = models.UUIDField(default=uuid.uuid4)
    method = models.CharField(max_length=10, choices=PurchaseMethod, default=ONEOFF)
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    price = models.FloatField()

class RegularPayment(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    serial = models.ForeignKey('product.ProductSerial', on_delete=models.CASCADE, blank=False)
    billing_info = models.ForeignKey('order.BillingInfo', on_delete=models.SET_NULL, null=True, blank=True)
    policy = models.ForeignKey('order.PricingPolicy', on_delete=models.SET_NULL, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
