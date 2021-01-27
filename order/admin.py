from django.contrib import admin
from .models import BillingInfo

# Register your models here.
@admin.register(BillingInfo)
class Test(admin.ModelAdmin):
    list_display = ('billing_key', 'user', )
    list_filter = ('user',)