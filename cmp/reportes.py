import os
from django import forms
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

from .models import ComprasEncabezado, ComprasDetalle
from django.utils import timezone

def link_callback(uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        result = finders.find(uri)
        if result:
                if not isinstance(result, (list, tuple)):
                        result = [result]
                result = list(os.path.realpath(path) for path in result)
                path=result[0]
        else:
                sUrl = settings.STATIC_URL        # Typically /static/
                sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
                mUrl = settings.MEDIA_URL         # Typically /media/
                mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

                if uri.startswith(mUrl):
                        path = os.path.join(mRoot, uri.replace(mUrl, ""))
                elif uri.startswith(sUrl):
                        path = os.path.join(sRoot, uri.replace(sUrl, ""))
                else:
                        return uri

        # make sure that file exists
        if not os.path.isfile(path):
                raise Exception(
                        'media URI must start with %s or %s' % (sUrl, mUrl)
                )
        return path


def reporte_compras(request):
    template_path='cmp/compras_print_all.html'
    today = timezone.now()

    compras = ComprasEncabezado.objects.all()
    context = {
        'obj':compras,
        'today': today,
        'request':request
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="todas_las_compras.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('Ha ocurrido un error <pre>' + html + '</pre>')
    return response


def reporte_compra(request, compra_id):
    template_path='cmp/compras_print_one.html'
    today = timezone.now()

    encabezado = ComprasEncabezado.objects.filter(id=compra_id).first()

    if encabezado:
        detalle = ComprasDetalle.objects.filter(compra_id=compra_id)
    else:
        detalle = {}

    context = {
        'detalle':detalle,
        'encabezado':encabezado,
        'today': today,
        'request':request
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reporte_compra.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('Ha ocurrido un error <pre>' + html + '</pre>')
    return response
