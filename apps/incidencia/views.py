import xlwt
import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.utils import timezone

from .forms import DetalleForm
from .models import Incidencia, DetalleIncidencia
from apps.cliente.models import Cliente
from usuario.models import Asesor, BackOffice

# Create your views here.


def buscar_incidencia(request, data):
    """ Busca incidencia por su ID, y muestra su informacion """

    contexto = {}
    if request.user.is_staff is True:
        return redirect('logout')

    try:
        incidencia = Incidencia.objects.get(id=data)
    except:
        incidencia = None

    if incidencia is not None:
        contexto['incidencia'] = incidencia
        contexto['user'] = request.user
        detalle = DetalleIncidencia.objects.filter(incidencia=incidencia)

        if incidencia.estado is True:
            contexto['back'] = True

        if request.user.is_asesor is False:
            contexto['cerrar'] = True

        if incidencia.cliente.dni == '':
            contexto['empresa'] = True

        if detalle.count() > 0:
            contexto['detalle'] = detalle

    return render(request, 'incidencia/incidencia_encontrada.html', contexto)


def generar_incidencia(request, clid):
    """ Crea incidencia mediante el ID del cliente """

    if request.user.is_staff is True:
        return redirect('logout')
    try:
        cliente = Cliente.objects.get(id=clid)
    except:
        cliente = None

    try:
        asesor = Asesor.objects.get(usuario=request.user)
    except:
        asesor = None

    if request.user.is_asesor is False:
        return redirect('usuario:perfil_usuario')

    if cliente is not None:
        incidencia = Incidencia(cod_asesor=asesor, cliente=cliente)
        incidencia.save()

    if cliente.ruc is not '':
        data = cliente.ruc
    else:
        data = cliente.dni

    return redirect('cliente:buscar_cliente', data=data)


class RegistrarDetalle(CreateView):
    """ Crea detalle por incidenica, el metodo
    get_context_data: Prepara la data a transmitir
    get: Recibe peticion del usuario para enviar el formulario detalle
    post: Recibe el formulario llenado y lo valida y registra """

    model = DetalleIncidencia
    form_class = DetalleForm
    template_name = 'incidencia/detalle_incidencia.html'
    success_url = 'incidencia:buscar_incidencia'

    def get_context_data(self, **kwargs):
        context = super(RegistrarDetalle, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        context['id'] = pk
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object
        if request.user.is_staff is True:
            return redirect('logout')
        form = self.form_class(self.request.GET)
        return self.render_to_response(self.get_context_data(form=form,
                                                             user=request.user))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(self.request.POST)
        if form.is_valid():
            detalle = form.save(commit=False)
            detalle.incidencia = Incidencia.objects.get(id=kwargs['pk'])
            detalle.usuario = request.user
            detalle.save()
            return redirect(self.get_success_url(), data=kwargs['pk'])
        return self.render_to_response(self.get_context_data(form=form,
                                                             user=request.user))


def cerrar_incidencia(request, incid):
    """ Genera el cierre de incidencia por el ID de la incidencia """

    if request.user.is_staff is True:
        return redirect('logout')
    try:
        incidencia = Incidencia.objects.get(id=incid)
    except:
        incidencia = None

    try:
        back = BackOffice.objects.get(usuario=request.user)
    except:
        back = None

    if incidencia is not None and request.user.is_asesor is False:
        incidencia.cod_back = back
        incidencia.fecha_cierre = timezone.localtime(timezone.now())
        incidencia.estado = True
        incidencia.save()
        return redirect('incidencia:buscar_incidencia', data=incid)

    return redirect('usuario:perfil_usuario')



def exportar_reporte(request, desde, hasta):
    """ Genera el reporte en Excel mediante las fechas desde-hasta """

    if request.user.is_staff is True:
        return redirect('logout')

    if request.user.is_asesor is True:
        return redirect('usuario:perfil_usuario')

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="reporte.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Reporte')
    row_num = 0
    col_width = 256 * 40

    font_style = get_estilo(True)

    incidencias = get_incidencias(desde, hasta)
    if incidencias is None:
        return redirect('usuario:perfil_usuario')
    detalles = get_detalles(incidencias)
    mayor = 0
    for posi in detalles:
        if len(posi) > mayor:
            mayor = len(posi)

    columns = [
        'ID', 'Estado', 'Fecha Creacion', 'Asesor', 'Fecha de cierre',
        'BackOffice', 'Ruc o DNI cliente', 'Cliente', 'Servicios'
    ]

    for pos in range(mayor):
        columns.append('Detalle ' + str(pos+1))

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
        ws.col(col_num).width = col_width

    font_style = get_estilo(False)

    col_num = 0
    for inci in incidencias:
        row_num += 1
        asesor = get_data_individuo(asesor_d=inci.cod_asesor)
        cliente = get_data_individuo(cliente_d=inci.cliente)
        fecha_cierre = get_fecha(inci.fecha_cierre)
        estado = get_estado(inci.estado)
        if inci.cod_back is not None:
            back = get_data_individuo(back_d=inci.cod_back)
        else:
            back = ''
        ws.write(row_num, col_num, inci.id, font_style)
        ws.write(row_num, col_num+1, estado, font_style)
        ws.write(row_num, col_num+2, str(inci.fecha_generada)[0:10], font_style)
        ws.write(row_num, col_num+3, asesor, font_style)
        ws.write(row_num, col_num+4, fecha_cierre, font_style)
        ws.write(row_num, col_num+5, back, font_style)
        ws.write(row_num, col_num+6, cliente[0][1:], font_style)
        ws.write(row_num, col_num+7, cliente[1], font_style)
        ws.write(row_num, col_num+8, cliente[2], font_style)

        det_pos = 0
        for recorrer in detalles[row_num-1]:
            ws.write(row_num, (col_num+9+det_pos),
                     recorrer.detalle, font_style)
            det_pos += 1

    wb.save(response)
    return response


def get_incidencias(desde, hasta):
    """ Obtiene las incidencias mediante el rango de fechas """
    # start = datetime.date(int(desde[4:]), int(desde[2:4]), int(desde[0:2]))
    # end = datetime.date(int(hasta[4:]), int(hasta[2:4]), int(hasta[0:2]))
    start = desde[4:] + "-" + desde[2:4] + "-" + desde[0:2]
    end = hasta[4:] + "-" + hasta[2:4] + "-" + hasta[0:2]
    cond = "fecha_generada >= '" + start + "' and "
    cond += "fecha_generada < '" + end + "'"

    #incidencia = Incidencia.objects.filter(fecha_generada__date__range=(start,end)).order_by('id')
    incidencia = Incidencia.objects.extra(where=[cond])

    if incidencia.count() < 1:
        return None
    return incidencia


def get_detalles(incidencias):
    """ Obtiene el detalle de cada incidencia """
    detalles = []
    for x in incidencias:
        detalle = DetalleIncidencia.objects.filter(incidencia=x).order_by('incidencia')
        detalles.append(detalle)
    return detalles


def get_data_individuo(asesor_d=None, back_d=None, cliente_d=None):
    """ Modela la informacion del asesor, back y/o cliente que sera
    mostrada en el excel """
    if asesor_d is not None:
        usuario = asesor_d.usuario.nombre
        usuario += ' ' + asesor_d.usuario.ape_pat
        usuario += ' ' + asesor_d.usuario.ape_mat
        return usuario
    elif back_d is not None:
        usuario = back_d.usuario.nombre
        usuario += ' ' + back_d.usuario.ape_pat
        usuario += ' ' + back_d.usuario.ape_mat
        return usuario
    elif cliente_d is not None:
        cliente = []
        servicio = ''
        if cliente_d.ruc != '':
            cliente.append(cliente_d.ruc)
            cliente.append(cliente_d.razon_social)
        else:
            cliente.append(cliente_d.dni)
            nombres = cliente_d.nombre
            nombres += ' ' + cliente_d.ape_pat
            nombres += ' ' + cliente_d.ape_mat
            cliente.append(nombres)
        for x in cliente_d.servicio.all():
            servicio += x.servicio + ' '
        cliente.append(servicio)
        return cliente
    else:
        return None


def get_fecha(fecha):
    """ Modela las fechas que seran mostradas en el excel """
    if fecha is None:
        return ''
    else:
        return str(fecha)[0:10]

def get_estado(estado):
    """ Modela el estado de la incidencia para ser mostrada en el excel """
    if estado is True:
        return 'Cerrado'
    else:
        return 'Generado'


def get_estilo(tipo):
    """ Genera el estilo que va a tener el excel como la fuente,
    el tamaño, etc """
    font_style = xlwt.XFStyle()
    font_style.borders.bottom = xlwt.Borders.HAIR
    font_style.borders.top = xlwt.Borders.HAIR
    font_style.borders.left = xlwt.Borders.HAIR
    font_style.borders.right = xlwt.Borders.HAIR
    font_style.font.height = 220
    if tipo is True:
        font_style.font.bold = True
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = xlwt.Style.colour_map['coral']
        font_style.pattern = pattern
    else:
        font_style.font.bold = False
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = xlwt.Style.colour_map['ivory']
        font_style.pattern = pattern
    return font_style
