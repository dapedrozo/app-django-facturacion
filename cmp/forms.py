from django import forms
from django.db import models
from django.forms import fields, widgets
from .models import Proveedor, ComprasEncabezado

class ProveedorForm(forms.ModelForm):
    email = forms.EmailField(max_length=250)
    class Meta:
        model = Proveedor
        exclude = ['user_modifi','fecha_modif','user_crea','fecha_crea']
        widget = {'descripcion':forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })


class ComprasEncabezadoForm(forms.ModelForm):
    fecha_comra = forms.DateInput()
    fecha_factura = forms.DateInput()

    class Meta:
        model = ComprasEncabezado
        fields = ['proveedor','fecha_compra','observaciones','no_factura','fecha_factura','sub_total','descuento','total']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })
        self.fields['fecha_compra'].widget.attrs['readonly'] = True
        self.fields['fecha_factura'].widget.attrs['readonly'] = True
        self.fields['sub_total'].widget.attrs['readonly'] = True
        self.fields['descuento'].widget.attrs['readonly'] = True
        self.fields['total'].widget.attrs['readonly'] = True