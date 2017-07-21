from django.shortcuts import render, redirect

from .models import Asesor, BackOffice
from apps.incidencia.models import Incidencia, DetalleIncidencia
# Create your views here.


def perfil_usuario(request):
    """ Obtiene informacion del usuario logueado y lo muestra  """
    usuario = request.user
    contexto = {}
    contexto['perfil'] = usuario
    tuser = None

    if usuario.is_staff is True:
        return redirect('logout')

    if usuario.is_asesor is True:
        try:
            contexto['asesor'] = Asesor.objects.get(usuario=usuario)
            tuser = contexto['asesor']
        except:
            contexto['vacio'] = None
    else:
        try:
            contexto['back'] = BackOffice.objects.get(usuario=usuario)
            tuser = contexto['back']
        except:
            contexto['vacio'] = None

    lista = get_incidencia_atendidas(usuario, tuser)

    if len(lista) > 0:
        contexto['ultimos'] = lista

    return render(request, 'perfil_usuario.html', contexto)


def takeFecha(elem):
    """ Para recorrer arrays """
    return elem[3]


def get_incidencia_atendidas(user, tuser):
    """ Obtiene la incidencia mas reciente donde colaboro el usuario
    logueado """
    if user.is_asesor is True:
        incidencias = Incidencia.objects.filter(cod_asesor=tuser). \
            order_by('-id')[:1]
    else:
        incidencias = Incidencia.objects.filter(cod_back=tuser). \
            order_by('-id')[:1]

    detalles = DetalleIncidencia.objects.filter(usuario=user). \
        order_by('-id')[:1]

    lista = []

    if len(incidencias) == 0 and len(detalles) == 0:
        return lista

    if len(incidencias) > 0:
        lista.append([incidencias[0].id, incidencias[0].cliente,
                      incidencias[0].estado, incidencias[0].fecha_generada])

    if len(detalles) > 0:
        lista.append([detalles[0].incidencia.id, detalles[0].incidencia.cliente,
                  detalles[0].incidencia.estado, detalles[0].fecha_generada])

    sortedList = sorted(lista, key=takeFecha, reverse=True)

    return sortedList[:1]
