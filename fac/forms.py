from django import forms
from django.db import models
from django.forms import fields, widgets
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombres','apellidos','tipo','celular','estado']
        exclude = ['user_modifi','fecha_modif','user_crea','fecha_crea']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })

