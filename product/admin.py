from django.contrib import admin
from product.models import Product, ProductSerial, ProductSerial_batch
from django.contrib.auth.models import User
from django.contrib.contenttypes.admin import GenericStackedInline
# Register your models here.
from taggit.models import TaggedItem

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

@admin.register(ProductSerial_batch)
class SerialBatchInstanceAdmin(admin.ModelAdmin):
    pass
    # list_display = ('name', 'date', 'tags')
    # list_filter = ('name', 'date', 'tags')


# class UserInfoInline(admin.StackedInline):
#     model = ProductSerial_batch
#     field = ('tag_list')

#     def get_queryset(self, request):
#         return super().get_queryset(request).prefetch_related('tags')
    
#     def tag_list(self, obj):
#         return u", ".join(o.name for o in obj.tags.all())

# class UserInstanceAdmin(admin.ModelAdmin):
#     inlines = [UserInfoInline]
#     list_display = ('username', 'email', 'is_active', 'tag_list')

#     def tag_list(self, obj):
#         return UserInfoInline.tag_list(self, UserInfo.objects.get(user=obj))
