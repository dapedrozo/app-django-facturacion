from django.urls import path
from .views import CategoriaView, CategoriaNew, CategoriaEdit, CategoriaDel, SubCategoriaView, SubCategoriaNew, SubCategoriaEdit, SubCategoriaDel, MarcaView, MarcaNew, MarcaEdit, MarcaInactivate, UnidadMedidaView, UnidadMedidaNew, UnidadMedidaEdit, UnidadMedidaInactivate, ProductoView, ProductoNew, ProductoEdit, ProductoInactivate

urlpatterns = [
    path('categorias/',CategoriaView.as_view(), name='categoria_list'),
    path('categorias/new',CategoriaNew.as_view(), name='categoria_new'),
    path('categorias/edit/<int:pk>',CategoriaEdit.as_view(), name='categoria_edit'),
    path('categorias/delete/<int:pk>',CategoriaDel.as_view(), name='categoria_del'),

    path('subcategorias/',SubCategoriaView.as_view(), name='subcategoria_list'),
    path('subcategorias/new',SubCategoriaNew.as_view(), name='subcategoria_new'),
    path('subcategorias/edit/<int:pk>',SubCategoriaEdit.as_view(), name='subcategoria_edit'),
    path('subcategorias/delete/<int:pk>',SubCategoriaDel.as_view(), name='subcategoria_del'),

    path('marcas/',MarcaView.as_view(), name='marca_list'),
    path('marcas/new',MarcaNew.as_view(), name='marca_new'),
    path('marcas/edit/<int:pk>',MarcaEdit.as_view(), name='marca_edit'),
    path('marcas/inactivate/<int:id>',MarcaInactivate, name='marca_inactivate'),

    path('unidades-medida/',UnidadMedidaView.as_view(), name='unidadmedida_list'),
    path('unidades-medida/new',UnidadMedidaNew.as_view(), name='unidadmedida_new'),
    path('unidades-medida/edit/<int:pk>',UnidadMedidaEdit.as_view(), name='unidadmedida_edit'),
    path('unidades-medida/inactivate/<int:id>',UnidadMedidaInactivate, name='unidadmedida_inactivate'),

    path('productos/',ProductoView.as_view(), name='producto_list'),
    path('productos/new',ProductoNew.as_view(), name='producto_new'),
    path('productos/edit/<int:pk>',ProductoEdit.as_view(), name='producto_edit'),
    path('productos/inactivate/<int:id>',ProductoInactivate, name='producto_inactivate'),
]
