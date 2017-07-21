from django.shortcuts import render
from .models import Cliente

from apps.incidencia.models import Incidencia

# Create your views here.


def buscar_cliente(request, data):
    """ OBtiene informacion del cliente a buscar para ser mostrada """
    contexto = {}
    if len(data) == 8:
        try:
            cliente = Cliente.objects.get(dni=data)
            contexto['persona'] = True
        except:
            cliente = None
    else:
        try:
            cliente = Cliente.objects.get(ruc=data)
        except:
            cliente = None

    if cliente is not None:
        contexto['no_mas_incidencia'] = False
        contexto['user'] = request.user
        contexto['cliente'] = cliente
        incidencia = Incidencia.objects.filter(cliente=cliente).order_by('-id')

        if request.user.is_asesor is True:
            contexto['asesor'] = True

        if incidencia.count() > 0:
            if incidencia[0].estado is False:
                contexto['no_mas_incidencia'] = True
            if incidencia.count() == 5:
                contexto['incidencias'] = incidencia[0:5]
            elif incidencia.count() < 5:
                contexto['incidencias'] = incidencia[0:incidencia.count()]

    return render(request, 'cliente/cliente_encontrado.html', contexto)
