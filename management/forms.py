import datetime


from django import forms

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

