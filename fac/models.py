from django.db import models
from bases.models import ClaseModelo


class Cliente(ClaseModelo):
    #choice para definir si es p.natural o juridica
    #se define las variables de las opciones y se guardan en una lista para usar a la hora del renderizado
    NAT='Natural'
    JUR = 'Juridica'
    TIPO_CLIENTE = [
        (NAT,'Natural'),
        (JUR,'Juridica')
    ]

    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    celular = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )
    tipo = models.CharField(
        max_length=10,
        choices=TIPO_CLIENTE,
        default=NAT
    )

    def __str__(self):
        return '{} {}'.format(self.apellidos, self.nombres)

    def save(self):
        self.nombres = self.nombres.upper()
        self.apellidos = self.apellidos.upper()
        super(Cliente, self).save()

    class Meta:
        verbose_name_plural = 'Clientes'