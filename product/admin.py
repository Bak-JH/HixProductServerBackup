from django.contrib import admin
from product.models import Product, ProductSerial, ProductSerial_batch
from django.contrib.auth.models import User
from django.contrib.contenttypes.admin import GenericStackedInline
# Register your models here.

class SerialBatchInline(admin.StackedInline):
    model = ProductSerial_batch

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def batch_name(self, obj):
        return obj.name

    def batch_date(self,obj):
        return obj.date

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())

@admin.register(ProductSerial)
class ProductSerialInstanceAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'owner', 'product', 'created_date', 'expire_date', 'batch_name', 'batch_date', 'tag')
    list_filter = ('serial_number', 'owner', 'product', 'created_date', 'expire_date')

    def batch_name(self, obj):
        return SerialBatchInline.batch_name(self, obj.batch)

    def batch_date(self, obj):
        return SerialBatchInline.batch_date(self, obj.batch)

    def tag(self, obj):
        return SerialBatchInline.tag_list(self, obj.batch)

    def get_form(self, request, obj=None, **kwargs):
        form = super(ProductSerialInstanceAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['batch'].label_from_instance = lambda obj: "{}".format(obj.name)
        return form

@admin.register(Product)
class ProductInstanceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)

@admin.register(ProductSerial_batch)
class SerialBatchInstanceAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'tag_list')
    list_filter = ('name', 'date')

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())
