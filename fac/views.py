from typing import Coroutine, KeysView
from django.shortcuts import redirect, render
from django.views import generic
from django.urls import reverse_lazy
import datetime

from django.http import HttpResponse
import json
from django.db.models import Sum

from .models import Cliente

#mensajes para funciones
from django.contrib import messages
#mensajes para clases
from django.contrib.messages.views import SuccessMessageMixin
#para pasarle la funcion sin privilegios a clases
from bases.views import SinPrivilegios
#para pasarle la funcion login y permission a las funciones
from django.contrib.auth.decorators import login_required, permission_required

class ClienteView(SinPrivilegios, generic.ListView):
    permission_required = 'fac.view_cliente'
    model = Cliente
    template_name = 'fac/cliente_list.html'
    context_object_name = 'obj'
