from django.contrib import admin
from django.contrib import admin
from product.models import Product, ProductSerial

# Register your models here.

@admin.register(ProductSerial)
class ProductSerialInstanceAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'owner', 'product', 'created_date', 'expire_date')
    list_filter = ('serial_number', 'owner', 'product', 'created_date', 'expire_date')
    def product_name(self, product_serial):
        return product_serial.product.name


@admin.register(Product)
class ProductInstanceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
