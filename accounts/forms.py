from django import forms

class PasswordChangeForm(forms.Form):
    username = forms.CharField(error_messages="Username not matching.",required=True)
    password = forms.CharField(widget = forms.PasswordInput(),error_messages="Enter current password.",required=True)
    New_password = forms.CharField(widget = forms.PasswordInput(),help_text="<p>* Your password can’t be too similar to your other personal information.</p><p>* Your password must contain at least 8 characters.</p><p>* Your password can’t be a commonly used password.</p><p>* Your password can’t be entirely numeric.</p>",required=True)
    
    