from django.contrib import admin
from django.conf.locale.es import formats as es_formats

from resin.models import Material, PrintSetting


admin.site.register(Material)
admin.site.register(PrintSetting)



# Register your models here.
# es_formats.DATETIME_FORMAT = "d M Y H:i:s"

# class MaterialAdmin(admin.ModelAdmin):
#     	list_display = ['M_id','led_offset','last_update']

# admin.site.register(Material,MaterialAdmin)