from accounts.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field



class CreateSubUserForm2(forms.Form):
    company = forms.CharField(label='Company and Address',widget=forms.Textarea(attrs={'cols': 80, 'rows': 4}),required=False)
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Confirm Password',widget=forms.PasswordInput())
    password1 = None # Standard django password input
    password2 = None # Standard django password confirmation input
    def clean(self):
        cleaned_data = super(CreateSubUserForm2, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "Password does not match")

        return cleaned_data

class CreateSubUserForm1(UserCreationForm):
    password1 = None # Standard django password input
    password2 = None # Standard django password confirmation input
    class Meta:
        model = User
        fields = ['username','phone','first_name','email']
        labels = {
            'first_name': ('Sub-User Name'),
            }
    
    

