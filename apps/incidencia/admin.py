from django.contrib import admin

# Register your models here.


# Modela como se vera los modelos en el panel Administrativo
class CustomIncidencia(admin.ModelAdmin):
    list_display = ('id', 'cod_asesor', 'cod_back', 'cliente',
                    'fecha_generada', 'fecha_cierre', 'estado')
    list_filter = ('id', 'fecha_generada', 'fecha_cierre', 'estado')
    search_fields = ('id', 'cod_asesor__usuario__usuario',
    'cod_back__usuario__usuario', 'cliente__id')
    ordering = ('id', 'fecha_generada', 'fecha_cierre')


class CustomDetalleIncidencia(admin.ModelAdmin):
    list_display = ('id', 'incidencia', 'usuario', 'detalle', 'fecha_generada')
    list_filter = ('id', 'incidencia', 'usuario', 'fecha_generada')
    search_fields = ('id', 'incidencia__id', 'usuario__usuario',
    'fecha_generada')
    ordering = ('id', 'fecha_generada')
