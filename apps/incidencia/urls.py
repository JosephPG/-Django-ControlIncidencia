from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import (buscar_incidencia, generar_incidencia, RegistrarDetalle,
                    cerrar_incidencia, exportar_reporte)

# Genera url para las funciones, buscar_incidencia, generar_incidencia,
# RegistrarDetalle, cerrar_incidencia, exportar_reporte 
urlpatterns = [
    url(r'^buscar-incidencia/(?P<data>\d+)/$',
        login_required(buscar_incidencia),
        name="buscar_incidencia"),
    url(r'^generar-incidencia/(?P<clid>\d+)/$',
        login_required(generar_incidencia),
        name="generar_incidencia"),
    url(r'^registrar-detalle/(?P<pk>\d+)$',
        login_required(RegistrarDetalle.as_view()),
        name="registrar_detalle"),
    url(r'^cerrar-incidencia/(?P<incid>\d+)$',
        login_required(cerrar_incidencia),
        name="cerrar_incidencia"),
    url(r'^exportar-reporte/(?P<desde>\d+)/(?P<hasta>\d+)/$',
        login_required(exportar_reporte),
        name="exportar_reporte"),
]
