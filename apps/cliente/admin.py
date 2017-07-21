from django.contrib import admin

# Register your models here.


# Modela como se vera los modelos en el panel administrativo
class CustomCliente(admin.ModelAdmin):
    list_display = ('id', 'ruc', 'dni', 'nombre', 'ape_pat', 'ape_mat',
                    'razon_social')
    list_filter = ('id', 'ruc', 'dni')
    search_fields = ('id', 'ruc', 'dni')
    ordering = ('id',)


class CustomTipoServicio(admin.ModelAdmin):
    list_display = ('id', 'servicio')
    list_filter = ('id', 'servicio')
    search_fields = ('id', 'servicio')
    ordering = ('id',)
