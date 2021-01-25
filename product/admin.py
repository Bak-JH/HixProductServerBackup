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
    list_display = ('serial_number', 'owner', 'product', 'created_date', 'expire_date', 'tag')
    list_filter = ('serial_number', 'owner', 'product', 'created_date', 'expire_date')

    def tag(self, obj):
        return SerialBatchInline.batch_name(self, obj.batch)

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
