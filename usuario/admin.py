from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Usuario, BackOffice, Asesor

from apps.cliente.models import Cliente, TipoServicio
from apps.cliente.admin import CustomCliente, CustomTipoServicio

from apps.incidencia.models import Incidencia, DetalleIncidencia
from apps.incidencia.admin import CustomIncidencia, CustomDetalleIncidencia

# Register your models here.

# Generar modelos para que sean vistas y usadas en el panel administrativo
class CustomUserAdmin(UserAdmin):
    fieldsets = ()
    add_fieldsets = (
        (None, {
            'fields': ('nombre', 'ape_pat', 'ape_mat',
                       'usuario', 'password1', 'password2', 'is_asesor'),
        }),
    )
    list_display = ('usuario', 'is_active', 'is_asesor', 'is_staff')
    search_fields = ('usuario',)
    ordering = ('usuario',)


class CustomBackOffice(admin.ModelAdmin):
    fieldsets = ()
    list_display = ('id', 'usuario')
    list_filter = ('id', 'usuario')
    search_fields = ['id', 'usuario__usuario',]
    ordering = ('id',)


class CustomAsesor(admin.ModelAdmin):
    fieldsets = ()
    list_display = ('id', 'usuario')
    list_filter = ('id', 'usuario')
    search_fields = ['id', 'usuario__usuario']
    ordering = ('id',)


admin.site.register(TipoServicio, CustomTipoServicio)
admin.site.register(Cliente, CustomCliente)
admin.site.register(Usuario, CustomUserAdmin)
admin.site.register(BackOffice, CustomBackOffice)
admin.site.register(Asesor, CustomAsesor)
admin.site.register(Incidencia, CustomIncidencia)
admin.site.register(DetalleIncidencia, CustomDetalleIncidencia)
