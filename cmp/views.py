
from typing import Coroutine, KeysView
from django.shortcuts import redirect, render
from django.views import generic
from django.urls import reverse_lazy
import datetime

from django.http import HttpResponse
import json
from django.db.models import Sum

from .models import Proveedor, ComprasEncabezado, ComprasDetalle
from inv.models import Producto
from .forms import ProveedorForm, ComprasEncabezadoForm

#mensajes para funciones
from django.contrib import messages
#mensajes para clases
from django.contrib.messages.views import SuccessMessageMixin
#para pasarle la funcion sin privilegios a clases
from bases.views import SinPrivilegios
#para pasarle la funcion login y permission a las funciones
from django.contrib.auth.decorators import login_required, permission_required

class ProveedorView(SinPrivilegios, generic.ListView):
    permission_required = 'cmp.view_proveedor'
    model = Proveedor
    template_name = 'cmp/proveedor_list.html'
    context_object_name = 'obj'


class ProveedorNew(SuccessMessageMixin, SinPrivilegios, generic.CreateView):
    permission_required = 'cmp.add_proveedor'
    model = Proveedor
    template_name = 'cmp/proveedor_form.html'
    context_object_name = 'obj'
    form_class = ProveedorForm
    success_message = 'Proveedor creado'
    success_url = reverse_lazy('cmp:proveedor_list')

    def form_valid(self, form):
        form.instance.user_crea = self.request.user
        return super().form_valid(form)


class ProveedorEdit(SuccessMessageMixin, SinPrivilegios, generic.UpdateView):
    permission_required = 'cmp.change_proveedor'
    model = Proveedor
    template_name = 'cmp/proveedor_form.html'
    context_object_name = 'obj'
    form_class = ProveedorForm
    success_message = 'Proveedor actualizado'
    success_url = reverse_lazy('cmp:proveedor_list')

    def form_valid(self, form):
        form.instance.user_modifi = self.request.user.id
        return super().form_valid(form)

@login_required(login_url='/login/')
@permission_required('cmp.change_proveedor',login_url='bases:sin_privilegios')
def ProveedorInactivate(request, id):
    template_name = 'cmp/cmp_del.html'
    contexto = {}
    proveedor = Proveedor.objects.filter(pk=id).first()

    if not proveedor:
        return HttpResponse('el proveedor no existe ' + str(id))

    if request.method == 'GET':
        contexto = {'obj': proveedor}

    if request.method == 'POST':
        proveedor.estado = False
        proveedor.save()
        messages.success(request, 'Proveedor inactivado')
        contexto = {'obj': 'OK'}
        return HttpResponse('proveedor inactivado')

    return render(request, template_name, contexto)


class ComprasView(SinPrivilegios, generic.ListView):
    permission_required = 'cmp.view_comprasencabezado'
    model = ComprasEncabezado
    template_name = 'cmp/compras_list.html'
    context_object_name = 'obj'


@login_required(login_url='/login/')
@permission_required('cmp.view_comprasencabezado',login_url='bases:sin_privilegios')
def Compras(request,compra_id=None):
    template_name = 'cmp/compras.html'
    productos = Producto.objects.filter(estado=True)
    form_compras = {}
    contexto = {}

    if request.method == 'GET':
        form_compras = ComprasEncabezadoForm()
        encabezado = ComprasEncabezado.objects.filter(pk = compra_id).first()

        #se envia el formulario con los valores inicializados si existieran
        if encabezado:
            detalle = ComprasDetalle.objects.filter(compra = encabezado)
            fecha_compra = datetime.date.isoformat(encabezado.fecha_compra)
            fecha_factura = datetime.date.isoformat(encabezado.fecha_factura)
            data = {
                'fecha_compra': fecha_compra,
                'proveedor': encabezado.proveedor,
                'fecha_factura': fecha_factura,
                'observaciones': encabezado.observaciones,
                'no_factura': encabezado.no_factura,
                'sub_total': encabezado.sub_total,
                'descuento': encabezado.descuento,
                'total': encabezado.total
            }
            form_compras = ComprasEncabezadoForm(data)
        else:
            detalle = None

        contexto = {'productos':productos, 'encabezado':encabezado, 'detalle':detalle, 'form_encabezado':form_compras}

    if request.method == 'POST':
        fecha_compra = request.POST.get('fecha_compra')
        observaciones = request.POST.get('observaciones')
        no_factura = request.POST.get('no_factura')
        fecha_factura = request.POST.get('fecha_factura')
        proveedor = request.POST.get('proveedor')
        sub_total = 0
        descuento = 0
        total = 0

        if not compra_id:
            prov = Proveedor.objects.get(pk=proveedor)
            enca = ComprasEncabezado(
                fecha_compra = request.POST.get('fecha_compra'),
                observaciones = request.POST.get('observaciones'),
                no_factura = request.POST.get('no_factura'),
                fecha_factura = request.POST.get('fecha_factura'),
                proveedor = prov,
                user_crea = request.user
            )
            
            if enca:
                enca.save()
                compra_id = enca.id
        else:
            enca = ComprasEncabezado.objects.filter(pk=compra_id).first()
            if enca:
                enca.fecha_compra = fecha_compra
                enca.observaciones = observaciones
                enca.no_factura = no_factura
                enca.fecha_factura = fecha_factura
                enca.user_modifi = request.user.id
                enca.save()

        if not compra_id:
            return redirect('cmp:compras_list')

        producto = request.POST.get('id_id_producto')
        cantidad = request.POST.get('id_cantidad_detalle')
        precio = request.POST.get('id_precio_detalle')
        sub_total_detalle = request.POST.get('id_sub_total_detalle')
        descuento_detalle = request.POST.get('id_descuento_detalle')
        total_detalle = request.POST.get('id_total_detalle')

        prod = Producto.objects.get(pk=producto)

        det = ComprasDetalle(
            compra = enca,
            producto = prod,
            cantidad = cantidad,
            precio_proveedor = precio,
            descuento = descuento_detalle,
            costo = 0,
            user_crea =  request.user
        )

        if det:
            det.save()
            
            sub_total = ComprasDetalle.objects.filter(compra=compra_id).aggregate(Sum('sub_total'))
            descuento = ComprasDetalle.objects.filter(compra=compra_id).aggregate(Sum('descuento'))
            enca.sub_total = sub_total['sub_total__sum']
            enca.descuento = descuento['descuento__sum']
            enca.save()

        return redirect('cmp:compras_edit',compra_id=compra_id)

    return render(request, template_name, contexto)


class ComprasDetalleDelete(SinPrivilegios, generic.DeleteView):
    permission_required = 'cmp.delete_comprasdetalle'
    model = ComprasDetalle
    template_name = 'cmp/compras_det_del.html'
    context_object_name = 'obj'

    def get_success_url(self):
        compra_id = self.kwargs['compra_id']
        return reverse_lazy('cmp:compras_edit', kwargs = {'compra_id':compra_id}) 