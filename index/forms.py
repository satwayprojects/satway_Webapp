from django import forms
from django.core.validators import RegexValidator


# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Layout, Submit, Field

class DateInput(forms.DateInput):
    input_type = 'date'

class AllocateDevice(forms.Form):
    username = forms.CharField(max_length=100,required=True,widget= forms.TextInput(attrs={'placeholder':'First 5 characters Username'}))
    allocate_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    imei = forms.CharField(max_length=15,min_length=15,validators=[RegexValidator(r'^\d{1,10}$')], help_text="IMEI to be allocated",required=False, widget= forms.TextInput
                           (attrs={'placeholder':'Enter 15 digit IMEI'}))