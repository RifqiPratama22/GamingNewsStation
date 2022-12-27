from django import forms
from django.contrib.auth.models import User
from .models import Biodata

class UserForms(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            "first_name" : forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type':'text',
                    'placeholder':'Nama Depan',
                    'required':True
                }),
            "last_name" : forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type':'text',
                    'placeholder':'Nama Belakang',
                    'required':True
                }),
            "email" : forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'rows':'text',
                    'placeholder':'Email',
                    'required':True
                }),
        }

class BiodataForms(forms.ModelForm):
    class Meta:
        model = Biodata
        fields = ('telp', 'alamat')
        widgets = {
            "telp" : forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type':'text',
                    'placeholder':'No Telepon',
                    'required':True
                }),
            "alamat" : forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type':'text',
                    'placeholder':'Alamat',
                    'required':True
                }),
        }