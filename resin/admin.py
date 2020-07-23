from django.contrib import admin
from django.conf.locale.es import formats as es_formats

from .models import Material

# Register your models here.
es_formats.DATETIME_FORMAT = "d M Y H:i:s"

class MaterialAdmin(admin.ModelAdmin):
    	list_display = ['M_id','led_offset','last_update']

admin.site.register(Material,MaterialAdmin)