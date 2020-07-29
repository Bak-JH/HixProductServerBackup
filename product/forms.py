import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from product.models import Product, ProductSerial
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column


class RegisterSerialForm(forms.Form):
    serial_number = forms.UUIDField(help_text="Enter product key")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(RegisterSerialForm, self).__init__(*args, **kwargs)

    def clean_serial_number(self):
        data = self.cleaned_data['serial_number']
        try:
            product_serial = ProductSerial.objects.get(serial_number=data)
        except:
            raise ValidationError(_('Invalid serial number - serial key does not exist'), code='invalid')

        if product_serial.owner == self.user:
            raise ValidationError(_('user already registered'), code='invalid')
        elif product_serial.owner is not None:
            raise ValidationError('Invalid serial number - serial already registered')

        return data


class LoginForm(forms.Form):
    id = forms.CharField(label="ID")
    password = forms.CharField(widget=forms.PasswordInput, label=_("Password"))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('id', css_class='form-group col-md-6 mb-0'),
                Column('password', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            )
        )
