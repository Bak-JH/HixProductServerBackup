import datetime


from django import forms
from product.models import Product
from datetime import date

# resin manager
class AddResinForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.product = kwargs.pop('resin')
        super(AddResinForm, self).__init__(*args, **kwargs)

    M_id = forms.CharField(max_length=50)
    bed_curing_layer = forms.IntegerField(initial=0)
    bed_curing_time = forms.IntegerField(initial=0)
    curing_time = forms.IntegerField(initial=0)
    layer_delay = forms.IntegerField(initial=0)
    z_hop_height = forms.IntegerField(initial=0)

    max_speed = forms.IntegerField(initial=0)
    init_speed = forms.IntegerField(initial=0)
    up_accel_speed = forms.IntegerField(initial=0)
    up_decel_speed = forms.IntegerField(initial=0)
    down_accel_speed = forms.IntegerField(initial=0)
    down_decel_speed = forms.IntegerField(initial=0)

    contraction_ratio = forms.FloatField(initial=0)
    led_offset = forms.FloatField(initial=0)

class AddProductSerialForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(AddProductSerialForm, self).__init__(*args, **kwargs)

    product = forms.ModelChoiceField(label="Product ", queryset=Product.objects.all())
    expire_date = forms.DateField(label="Expire Date ", input_formats=['%Y-%m-%d'], widget=forms.DateInput(attrs={'readonly':'readonly'}))
    number = forms.IntegerField(label="Number to Create ", initial=0)

