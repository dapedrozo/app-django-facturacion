from django.urls import path
from .views import ClienteView

urlpatterns = [
    path('clientes/',ClienteView.as_view(), name='cliente_list'),
    #path('proveedores/new',ProveedorNew.as_view(), name='proveedor_new'),
    #path('proveedores/edit/<int:pk>',ProveedorEdit.as_view(), name='proveedor_edit'),
    #path('proveedores/delete/<int:id>',ProveedorInactivate, name='proveedor_inactivate'),

]