from django.db import models
from bases.models import ClaseModelo
from inv.models import Producto
from django.db.models import Sum

#importar signals
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class Proveedor(ClaseModelo):
    descripcion = models.CharField(
        max_length=100,
        unique=True
    )
    direccion = models.CharField(
        max_length=250,
        null=True, 
        blank=True
    )
    contacto = models.CharField(
        max_length=100
    )
    telefono = models.CharField(
        max_length=10,
        null=True,
        blank=True
    )
    email = models.CharField(
        max_length=250,
        null=True,
        blank=True
    )

    def __str__(self):
        return '{}'.format(self.descripcion)

    def save(self):
        self.descripcion = self.descripcion.upper()
        super(Proveedor, self).save()

    class Meta:
        verbose_name_plural = 'Proveedores'


class ComprasEncabezado(ClaseModelo):
    fecha_compra = models.DateField(null=True, blank=True)
    observaciones = models.TextField(blank=True, null=True)
    no_factura = models.CharField(max_length=100)
    fecha_factura = models.DateField()
    sub_total = models.FloatField(default=0)
    descuento = models.FloatField(default=0)
    total = models.FloatField(default=0)

    proveedor = models.ForeignKey(Proveedor,on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.observaciones)

    def save(self):
        self.observaciones = self.observaciones.upper()
        self.total = self.sub_total - self.descuento
        super(ComprasEncabezado, self).save()

    class Meta:
        verbose_name_plural = 'Encabezado Compras'
        verbose_name = 'Encabezado Compra'


class ComprasDetalle(ClaseModelo):
    cantidad = models.BigIntegerField(default=0)
    precio_proveedor = models.FloatField(default=0)
    sub_total = models.FloatField(default=0)
    descuento = models.FloatField(default=0)
    total = models.FloatField(default=0)
    costo = models.FloatField(default=0)

    compra = models.ForeignKey(ComprasEncabezado, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.producto)

    def save(self):
        self.sub_total = float(float(int(self.cantidad)) * float(self.precio_proveedor))
        self.total = self.sub_total - float(self.descuento)
        super(ComprasDetalle, self).save()

    class Meta:
        verbose_name_plural = 'Detalle Compras'
        verbose_name = 'Detalle Compra'


@receiver(post_delete, sender=ComprasDetalle)
def detalle_compra_delete(sender, instance, **kwargs):
    #instancia es el objeto que se esta eliminando
    id_producto = instance.producto.id
    id_compra = instance.compra.id

    enca = ComprasEncabezado.objects.filter(pk=id_compra).first()
    if enca:
        sub_total = ComprasDetalle.objects.filter(compra=id_compra).aggregate(Sum('sub_total'))
        descuento = ComprasDetalle.objects.filter(compra=id_compra).aggregate(Sum('descuento'))
        enca.sub_total = sub_total['sub_total__sum']
        enca.descuento = descuento['descuento__sum']
        enca.save()

    producto = Producto.objects.filter(pk=id_producto).first()
    if producto:
        cantidad = int(producto.existencia)-int(instance.cantidad)
        producto.existencia = cantidad
        producto.save()


@receiver(post_save, sender=ComprasDetalle)
def detalle_compra_save(sender, instance, **kwargs):
    id_producto = instance.producto.id
    fecha_compra = instance.compra.fecha_compra

    producto = Producto.objects.filter(pk=id_producto).first()
    if producto:
        cantidad = int(producto.existencia)+int(instance.cantidad)
        producto.existencia = cantidad
        producto.ultima_compra = fecha_compra
        producto.save()
