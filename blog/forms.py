from dataclasses import field, fields
from django import forms
from django.forms import widgets
from .models import Artikel

class ArtikelForms(forms.ModelForm):
    class Meta:
        model = Artikel
        fields = ('judul', 'body', 'kategori', 'thumbnail')
        widgets = {
            "judul" : forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type':'text',
                    'placeholder':'Judul Artikel',
                    'required':True
                }),
            "body" : forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows':'4',
                    'placeholder':'Isi Deskripsi artikel',
                    'required':True
                }),
            "kategori" : forms.Select(
                attrs={
                    'class': 'form-control',
                    'type':'text',
                    'required':True
                }),
        }