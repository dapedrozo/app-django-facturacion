from django.contrib.messages.api import success
from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import generic
from .models import Categoria, SubCategoria, Marca, UnidadMedida, Producto
from .forms import CategoriaForm, SubCategoriaForm, MarcaForm, UnidadMedidaForm, ProductoForm
from django.urls import reverse_lazy
#mensajes para funciones
from django.contrib import messages
#mensajes para clases
from django.contrib.messages.views import SuccessMessageMixin
#para pasarle la funcion sin privilegios a clases
from bases.views import SinPrivilegios
#para pasarle la funcion login y permission a las funciones
from django.contrib.auth.decorators import login_required, permission_required


class CategoriaView(SinPrivilegios, generic.ListView):
    permission_required = 'inv.view_categoria'
    model = Categoria
    template_name = 'inv/categoria_list.html'
    context_object_name = 'obj'


class CategoriaNew(SuccessMessageMixin, SinPrivilegios, generic.CreateView):
    permission_required = 'inv.add_categoria'
    model = Categoria
    template_name = 'inv/categoria_form.html'
    context_object_name = 'obj'
    form_class = CategoriaForm
    success_message = 'Categoria creada'
    success_url = reverse_lazy('inv:categoria_list')

    def form_valid(self, form):
        form.instance.user_crea = self.request.user
        return super().form_valid(form)


class CategoriaEdit(SuccessMessageMixin, SinPrivilegios, generic.UpdateView):
    permission_required = 'inv.change_categoria'
    model = Categoria
    template_name = 'inv/categoria_form.html'
    context_object_name = 'obj'
    form_class = CategoriaForm
    success_message = 'Categoria actualizada'
    success_url = reverse_lazy('inv:categoria_list')

    def form_valid(self, form):
        form.instance.user_modifi = self.request.user.id
        return super().form_valid(form)


class CategoriaDel(SuccessMessageMixin, SinPrivilegios, generic.DeleteView):
    permission_required = 'inv.delete_categoria'
    model = Categoria
    template_name = 'inv/categoria_del.html'
    context_object_name = 'obj'
    success_message = 'Categoria eliminada'
    success_url = reverse_lazy('inv:categoria_list')


class SubCategoriaView(SinPrivilegios, generic.ListView):
    permission_required = 'inv.view_subcategoria'
    model = SubCategoria
    template_name = 'inv/subcategoria_list.html'
    context_object_name = 'obj'


class SubCategoriaNew(SuccessMessageMixin, SinPrivilegios, generic.CreateView):
    permission_required = 'inv.add_subcategoria'
    model = SubCategoria
    template_name = 'inv/subcategoria_form.html'
    context_object_name = 'obj'
    form_class = SubCategoriaForm
    success_message = 'Subcategoria creada'
    success_url = reverse_lazy('inv:subcategoria_list')

    def form_valid(self, form):
        form.instance.user_crea = self.request.user
        return super().form_valid(form)


class SubCategoriaEdit(SuccessMessageMixin, SinPrivilegios, generic.UpdateView):
    permission_required = 'inv.change_subcategoria'
    model = SubCategoria
    template_name = 'inv/subcategoria_form.html'
    context_object_name = 'obj'
    form_class = SubCategoriaForm
    success_message = 'Subcategoria actualizada'
    success_url = reverse_lazy('inv:subcategoria_list')

    def form_valid(self, form):
        form.instance.user_modifi = self.request.user.id
        return super().form_valid(form)


class SubCategoriaDel(SuccessMessageMixin, SinPrivilegios, generic.DeleteView):
    permission_required = 'inv.delete_subcategoria'
    model = SubCategoria
    template_name = 'inv/categoria_del.html'
    context_object_name = 'obj'
    success_message = 'Subcategoria eliminada'
    success_url = reverse_lazy('inv:subcategoria_list')


class MarcaView(SinPrivilegios, generic.ListView):
    permission_required = 'inv.view_marca'
    model = Marca
    template_name = 'inv/marca_list.html'
    context_object_name = 'obj'


class MarcaNew(SuccessMessageMixin, SinPrivilegios, generic.CreateView):
    permission_required = 'inv.add_marca'
    model = Marca
    template_name = 'inv/marca_form.html'
    context_object_name = 'obj'
    form_class = MarcaForm
    success_message = 'marca creada'
    success_url = reverse_lazy('inv:marca_list')

    def form_valid(self, form):
        form.instance.user_crea = self.request.user
        return super().form_valid(form)


class MarcaEdit(SuccessMessageMixin, SinPrivilegios, generic.UpdateView):
    permission_required = 'inv.change_marca'
    model = Marca
    template_name = 'inv/marca_form.html'
    context_object_name = 'obj'
    form_class = MarcaForm
    success_message = 'marca actializada'
    success_url = reverse_lazy('inv:marca_list')

    def form_valid(self, form):
        form.instance.user_modifi = self.request.user.id
        return super().form_valid(form)


@login_required(login_url='/login/')
@permission_required('inv.change_marca',login_url='bases:sin_privilegios')
def MarcaInactivate(request, id):
    marca = Marca.objects.filter(pk=id).first()
    contexto = {}
    template_name = 'inv/categoria_del.html'

    if not marca:
        return redirect('inv:marca_list')

    if request.method == 'GET':
        contexto = {'obj':marca}

    if request.method == 'POST':
        marca.estado = False
        marca.save()
        messages.success(request, 'Marca inactivada')
        return redirect('inv:marca_list')

    return render(request, template_name, contexto)


class UnidadMedidaView(SinPrivilegios, generic.ListView):
    permission_required = 'inv.view_unidadmedida'
    model = UnidadMedida
    template_name = 'inv/unidadmedida_list.html'
    context_object_name = 'obj'
    

class UnidadMedidaNew(SuccessMessageMixin, SinPrivilegios, generic.CreateView):
    permission_required = 'inv.add_unidadmedida'
    model = UnidadMedida
    template_name = 'inv/unidadmedida_form.html'
    context_object_name = 'obj'
    form_class = UnidadMedidaForm
    success_message = 'unidad de medida creada'
    success_url = reverse_lazy('inv:unidadmedida_list')

    def form_valid(self, form):
        form.instance.user_crea = self.request.user
        return super().form_valid(form)


class UnidadMedidaEdit(SuccessMessageMixin, SinPrivilegios, generic.UpdateView):
    permission_required = 'inv.change_unidadmedida'
    model = UnidadMedida
    template_name = 'inv/unidadmedida_form.html'
    context_object_name = 'obj'
    form_class = UnidadMedidaForm
    success_message = 'unidad de medida actualizada'
    success_url = reverse_lazy('inv:unidadmedida_list')

    def form_valid(self, form):
        form.instance.user_modifi = self.request.user.id
        return super().form_valid(form)


@login_required(login_url='/login/')
@permission_required('inv.change_unidadmedida',login_url='bases:sin_privilegios')
def UnidadMedidaInactivate(request, id):
    unidadMedida = UnidadMedida.objects.filter(pk=id).first()
    contexto = {}
    template_name = 'inv/categoria_del.html'

    if not unidadMedida:
        return redirect('inv:unidadmedida_list')

    if request.method == 'GET':
        contexto = {'obj':unidadMedida}

    if request.method == 'POST':
        unidadMedida.estado = False
        unidadMedida.save()
        messages.success(request, 'Unidad de medida inactivada')
        return redirect('inv:unidadmedida_list')

    return render(request, template_name, contexto)


class ProductoView(SinPrivilegios, generic.ListView):
    permission_required = 'inv.view_producto'
    model = Producto
    template_name = 'inv/producto_list.html'
    context_object_name = 'obj'


class ProductoNew(SuccessMessageMixin, SinPrivilegios, generic.CreateView):
    permission_required = 'inv.add_producto'
    model = Producto
    template_name = 'inv/producto_form.html'
    context_object_name = 'obj'
    form_class = ProductoForm
    success_message = 'producto creado'
    success_url = reverse_lazy('inv:producto_list')

    def form_valid(self, form):
        form.instance.user_crea = self.request.user
        return super().form_valid(form)


class ProductoEdit(SuccessMessageMixin, SinPrivilegios, generic.UpdateView):
    permission_required = 'inv.change_producto'
    model = Producto
    template_name = 'inv/producto_form.html'
    context_object_name = 'obj'
    form_class = ProductoForm
    success_message = 'producto actualizado'
    success_url = reverse_lazy('inv:producto_list')

    def form_valid(self, form):
        form.instance.user_modifi = self.request.user.id
        return super().form_valid(form)


@login_required(login_url='/login/')
@permission_required('inv.change_producto',login_url='bases:sin_privilegios')
def ProductoInactivate(request, id):
    producto = Producto.objects.filter(pk=id).first()
    contexto = {}
    template_name = 'inv/categoria_del.html'

    if not producto:
        return redirect('inv:producto_list')

    if request.method == 'GET':
        contexto = {'obj':producto}

    if request.method == 'POST':
        producto.estado = False
        producto.save()
        messages.success(request, 'Producto inactivada')
        return redirect('inv:producto_list')

    return render(request, template_name, contexto)