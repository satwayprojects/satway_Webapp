from django.core.validators import RegexValidator
from django.forms.widgets import PasswordInput
from accounts.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Layout, Submit, Field

###################################################################################################################

class CreateDistributerForm2(forms.Form):
    company = forms.CharField(label='Company and Address',widget=forms.Textarea(attrs={'cols': 80, 'rows': 4}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Confirm Password',widget=forms.PasswordInput())
    password1 = None # Standard django password input
    password2 = None # Standard django password confirmation input
    def clean(self):
        cleaned_data = super(CreateDistributerForm2, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        print(password,confirm_password)
        if password != confirm_password:
            self.add_error('confirm_password', "Password does not match.")

        return cleaned_data


class CreateDistributerForm1(UserCreationForm):  
    password1 = None # Standard django password input
    password2 = None # Standard django password confirmation input  
    class Meta:
        model = User
        fields = ['username','phone','first_name','email']
        labels = {
            'first_name': ('Distributor Name'),
            'last_name' : ('Address'),
        }
    

#########################################################################################################################

class DateInput(forms.DateInput):
    input_type = 'date'

class AllocateDevice(forms.Form):
    username = forms.CharField(max_length=100, widget= forms.TextInput(attrs={'placeholder':'First 5 characters of Distributer'}))
    allocate_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    imei = forms.CharField(max_length=15,min_length=15,validators=[RegexValidator(r'^\d{1,10}$')], help_text="IMEI to be allocated",required=False, widget= forms.TextInput
                           (attrs={'placeholder':'Enter 15 digit IMEI'}))