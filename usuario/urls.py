from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import perfil_usuario

# Genrar url para la funcion perfil_usuario
urlpatterns = [
    url(r'^perfil-usuario', login_required(perfil_usuario),
        name="perfil_usuario"),
]
