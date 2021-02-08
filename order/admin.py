from django.contrib import admin
from .models import BillingInfo, PricingPolicy

# Register your models here.
@admin.register(BillingInfo)
class Test(admin.ModelAdmin):
    list_display = ('billing_key', 'card_name', 'card_number')

@admin.register(PricingPolicy)
class Test(admin.ModelAdmin):
    pass
