from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(BillingInfo)
class BillingInfoInstanceAdmin(admin.ModelAdmin):
    list_display = ('billing_key', 'card_name', 'card_number')

@admin.register(PricingPolicy)
class PricingPolicyInstanceAdmin(admin.ModelAdmin):
    list_display = ('pricing_id', 'method', 'product', 'price')
    list_filter = ('method', 'product')

@admin.register(PaymentHistory)
class TesPaymentHistoryInstanceAdmin(admin.ModelAdmin):
    list_display = ('receipt_id', 'date', 'serial', 'billing_info', 'refunded')
    list_filter = ('date', 'serial', 'billing_info', 'refunded')

@admin.register(RegularPayment)
class tt(admin.ModelAdmin):
    pass
