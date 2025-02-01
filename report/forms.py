from django import forms

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=100, label="Ismingiz")
    password = forms.CharField(widget=forms.PasswordInput, label="Parolingiz")
