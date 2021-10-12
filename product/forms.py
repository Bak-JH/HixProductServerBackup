import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from product.models import Product, ProductSerial
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Field, HTML

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
    username = forms.CharField(label='ID')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column(
                    Field('username', css_class='form-control mb-4'),
                    css_class='col-sm-6'
                ),
                Column(
                    Field('password', css_class='form-control mb-4'),
                    css_class='col-sm-6'
                ),
                css_class='form-row'
            ),
            Row(
                Submit('submit', 'Sign in', css_class='btn btn-primary w-100 m-1'),
                css_class='form-row'
            )
        )

class SignupForm(forms.ModelForm):
    username = forms.CharField(label='ID')
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                 Column(
                    Field('email', css_class='form-control mb-4'),
                    css_class='col-sm-12'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    Field('username', css_class='form-control mb-4'),
                    css_class='col-sm-6'
                ),
               
                Column(
                    Field('password', css_class='form-control mb-4'),
                    css_class='col-sm-6'
                ),
                css_class='form-row'
            ),
            HTML('<input type="hidden" id="g-recaptcha-response" name="g-recaptcha-response">'),
            Row(
                Submit('submit', 'Sign up', css_class='btn btn-primary w-100 m-1'),
                css_class='form-row'
            )
        )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class ReauthPWForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column(
                    Field('password', css_class='form-control mb-4'),
                    css_class='col-sm-12'
                ),
            ),

            Row(
                Submit('submit', 'Submit', css_class='btn btn-primary w-100 m-1'),
                css_class='form-row'
            )
        )

    class Meta:
        model = User
        fields = ['password']

class ChangeUsernameForm(forms.ModelForm):
    username = forms.CharField(label='ID')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column(
                    Field('username', css_class='form-control mb-4'),
                    css_class='col-sm-12'
                ),
            ),

            Row(
                Submit('submit', 'Change username', css_class='btn btn-primary w-100 m-1'),
                css_class='form-row'
            )
        )

    class Meta:
        model = User
        fields = ['username']

class ChangeEmailForm(forms.ModelForm):
    email = forms.CharField(label='Email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column(
                    Field('email', css_class='form-control mb-4'),
                    css_class='col-sm-12'
                ),
            ),

            Row(
                Submit('submit', 'Change email', css_class='btn btn-primary w-100 m-1', onclick="\
                    if(email.value) {\
                        var reauth = confirm('Your account will be deactivated until re-authentication');\
                        if(!reauth) {\
                            return false;\
                        }\
                    }\
                "),
                css_class='form-row'
            )
        )

    class Meta:
        model = User
        fields = ['email']