from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import buscar_cliente

# Genera url para la funcion buscar_cliente
urlpatterns = [
    url(r'^buscar-cliente/(?P<data>\d+)/$', login_required(buscar_cliente),
        name="buscar_cliente"),
]
