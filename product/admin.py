from django.contrib import admin
from product.models import CrashFile, Product, ProductSerial, ProductSerial_batch
from django.contrib.auth.models import User
from django.contrib.contenttypes.admin import GenericStackedInline
# Register your models here.
from django.conf.urls import url
from django.urls import reverse
from django.http import HttpResponse
from django.utils.html import format_html

class SerialBatchInline(admin.StackedInline):
    model = ProductSerial_batch

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def batch_name(self, obj):
        if obj:
            return obj.name
        return ""

    def batch_date(self,obj):
        if obj:
            return obj.date
        return ""

    def tag_list(self, obj):
        if obj:
            return u", ".join(o.name for o in obj.tags.all())
        return ""

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

@admin.register(CrashFile)
class CrashFilesInstanceAdmin(admin.ModelAdmin):
    list_display = ('build_id', 'version', 'email', 'date', 'download_link')
    list_filter = ('version', 'email', 'date')

    # add custom view to urls
    def get_urls(self):
        urls = super(CrashFilesInstanceAdmin, self).get_urls()
        urls += [
            url(r'^download-file/(?P<pk>\d+)$', self.download_file, 
                name='applabel_modelname_download-file'),
        ]
        return urls

    # custom "field" that returns a link to the custom function
    def download_link(self, obj):
        dmp_filename = obj.dmp_file.name.split('/')[-1]
        return format_html(
            f'<a href="{{}}">{dmp_filename}</a>',
            reverse('admin:applabel_modelname_download-file', args=[obj.pk])
        )
    download_link.short_description = "Dump file"

    # add custom view function that downloads the file
    def download_file(self, request, pk):
        result_file = CrashFile.objects.get(pk=pk).dmp_file
        dmp_filename = result_file.name.split('/')[-1]
        response = HttpResponse(content_type='application/copntent')
        response['Content-Disposition'] = f'attachment; filename="{dmp_filename}"'
        # generate dynamic file content using object pk
        response.write(result_file.read())
        return response
