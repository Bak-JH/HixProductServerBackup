from django import forms
from django.core.exceptions import ValidationError

class CancelForm(forms.Form):
    cancel_user = forms.CharField(label='Canceller')
    cancel_reason = forms.CharField(label='Reason for cancellation', widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(CancelForm, self).__init__(*args, **kwargs)