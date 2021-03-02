from django.contrib import admin
from .models import BillingInfo, PricingPolicy, PaymentHistory

# Register your models here.
@admin.register(BillingInfo)
class Test(admin.ModelAdmin):
    list_display = ('billing_key', 'card_name', 'card_number')

@admin.register(PricingPolicy)
class Test(admin.ModelAdmin):
    pass

@admin.register(PaymentHistory)
class Test(admin.ModelAdmin):
    pass
