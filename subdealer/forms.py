from django.forms import models
from accounts.models import User, vehicleDetails
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field

###################################################################################################################
#########################################################################################################################


class CreateUserForm2(forms.Form):
    company = forms.CharField(label='Company and Address',widget=forms.Textarea(attrs={'cols': 80, 'rows': 4}),required=False)
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Confirm Password',widget=forms.PasswordInput())
    password1 = None # Standard django password input
    password2 = None # Standard django password confirmation input
    def clean(self):
        cleaned_data = super(CreateUserForm2, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "Password does not match")

        return cleaned_data

class CreateUserForm1(UserCreationForm):
    password1 = None # Standard django password input
    password2 = None # Standard django password confirmation input
    class Meta:
        model = User
        fields = ['username','phone','first_name','email']
        labels = {
            'first_name': ('User Name'),
            }
    
    

####################################################################################################


class DateInput(forms.DateInput):
    input_type = 'date'

class AllocateDevice(forms.Form):
    username = forms.CharField(max_length=100,widget= forms.TextInput(attrs={'placeholder':'Enter 4 characters of Username'}))
    allocate_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    imei = forms.CharField(max_length=15,min_length=15,validators=[RegexValidator(r'^\d{1,10}$')], help_text="IMEI to be allocated", widget= forms.TextInput
                           (attrs={'placeholder':'Enter 15 digit IMEI'}))


class AllocateDeviceUser(forms.Form):
    username = forms.CharField(max_length=100,required=True,widget= forms.TextInput(attrs={'placeholder':'Enter 4 characters of username'}))
    phone = forms.CharField(max_length=10, validators=[RegexValidator(r'^\d{1,10}$')], help_text="Phone number without Country Code")
    allocate_date = forms.DateField(label="Allocation Date",widget=forms.DateInput(attrs={'type': 'date'}))
    imei = forms.CharField(max_length=15,min_length=15,validators=[RegexValidator(r'^\d{1,15}$')], help_text="IMEI to be allocated",required=True, widget= forms.TextInput
                           (attrs={'placeholder':'Enter last 5 digits '}))


#####################################################################################################

class DeviceVehicleAllocationForm(models.ModelForm):
    installation_date = forms.DateField(label="Installaion Date",widget=forms.DateInput(attrs={'type': 'date'}))
    #imei = forms.DecimalField(max_digits=15,required=True)
    #imei = forms.CharField(label = "IMEI",max_length=15, min_length=15, validators=[RegexValidator(r'^\d{1,15}$')], help_text="15 Digit IMEI Number")
    class Meta:
        model = vehicleDetails
        fields = ['vehicle_no','odometer']
        labels = {
            'vehicle_no': ('Vehicle Registeration number'),
            'odometer' : ('Odometer Reading'),
        }
    
   
##############################################################################################################