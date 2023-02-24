from django.db import models
from django.contrib.auth.models import User

class ClaseModelo(models.Model):
    estado = models.BooleanField(default=True)
    fecha_crea = models.DateTimeField(auto_now_add=True)
    fecha_modif = models.DateTimeField(auto_now=True)
    user_crea =  models.ForeignKey(User, on_delete=models.CASCADE)
    user_modifi = models.IntegerField(blank=True, null=True)

    class Meta:
        abstract = True