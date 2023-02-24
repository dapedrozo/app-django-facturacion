from django import forms
from django.forms import fields, widgets
from .models import Categoria, SubCategoria, Marca, UnidadMedida, Producto

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['descripcion','estado']
        labels = {'descripcion':'Descripcion',
                  'estado':'estado'}
        widget = {'descripcion':forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })


class SubCategoriaForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.filter(estado=True).order_by('descripcion')
    )
    class Meta:
        model = SubCategoria
        fields = ['categoria','descripcion','estado']
        labels = {'descripcion':'subcategoria',
                  'estado':'estado'}
        widget = {'descripcion':forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })
        self.fields['categoria'].empty_label = 'Seleccione categoria'


class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = ['descripcion','estado']
        labels = {'descripcion':'marca',
                  'estado':'estado'}
        widget = {'descripcion':forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })


class UnidadMedidaForm(forms.ModelForm):
    class Meta:
        model = UnidadMedida
        fields = ['descripcion','estado']
        labels = {'descripcion':'Unidad de medida',
                  'estado':'estado'}
        widget = {'descripcion':forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['codigo','codigo_barras','descripcion','estado','precio','existencia','ultima_compra','marca','subcategoria','unidad_medida']
        exclude = ['user_modifi','fecha_modif','user_crea','fecha_crea']
        labels = {'codigo':'codigo','codigo_barras':'codigo barras','descripcion':'descripcion',
                  'estado':'estado','precio':'precio','existencia':'existencia','ultima_compra':'ultima compra','marca':'marca','subcategoria':'subcategoria','unidad_medida':'unidad medida'}
        widget = {'descripcion':forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })
        self.fields['ultima_compra'].widget.attrs['readonly'] = True
        self.fields['existencia'].widget.attrs['readonly'] = True