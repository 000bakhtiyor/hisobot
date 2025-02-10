from django import forms
from .models import *

from django import forms
from .models import Warehouse

class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = '__all__'
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'unit': forms.Select(attrs={'class': 'form-select'}),
            'arrival_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'additional_info': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class DebtorForm(forms.ModelForm):
    class Meta:
        model = Debtor
        fields = '__all__'
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'social_link': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image_url': forms.TextInput(attrs={'class': 'form-control'}),
            'user': forms.Select(attrs={'class': 'form-control'}),
        }

class ProductRequestForm(forms.ModelForm):
    class Meta:
        model = ProductRequest
        fields = '__all__'
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'required_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'measurement_unit': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=100, label="Ismingiz")
    password = forms.CharField(widget=forms.PasswordInput, label="Parolingiz")
