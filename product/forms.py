import datetime


from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from product.models import Product, ProductSerial

class RegisterSerialForm(forms.Form):

    serial_number = forms.UUIDField(help_text="Enter product key")

    def __init__(self,*args,**kwargs):
        self.product = kwargs.pop('product')
        super(RegisterSerialForm,self).__init__(*args,**kwargs)

    def clean_serial_number(self):
        data = self.cleaned_data['serial_number']
        try:
            product_serial = ProductSerial.objects.get(serial_number=data)
        except:
            raise ValidationError(_('Invalid serial number - serial key does not exist'))
        if(product_serial.owner is not None):
            raise ValidationError(_('Invalid serial number - serial already registered'))
        if(product_serial.product != self.product):
            raise ValidationError(_('Invalid serial number - serial for different product'))
        return data