from django.contrib import admin
from .models import CustomUser, Vehiculo, Celda, RegistroAsignacion, RegistroVehiculo, Usuario

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id_persona', 'nombre', 'tipo_doc', 'num_doc', 'telefono', 'correo', 'user_type')
    search_fields = ('nombre', 'num_doc', 'correo')
    list_filter = ('user_type',)

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('id_vehiculo', 'placa', 'tipo_vehiculo', 'marca', 'color', 'usuario')
    search_fields = ('placa', 'marca', 'color')
    list_filter = ('tipo_vehiculo',)

@admin.register(Celda)
class CeldaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'disponible')
    list_filter = ('disponible',)

@admin.register(RegistroAsignacion)
class RegistroAsignacionAdmin(admin.ModelAdmin):
    list_display = ('empleado', 'vehiculo_usuario', 'vehiculo', 'celda', 'fecha_asignacion')

    def vehiculo_usuario(self, obj):
        return obj.vehiculo.usuario
    vehiculo_usuario.short_description = 'Usuario'

@admin.register(RegistroVehiculo)
class RegistroVehiculoAdmin(admin.ModelAdmin):
    list_display = ('vehiculo', 'fecha_hora_ingreso', 'fecha_hora_salida')
    search_fields = ('vehiculo__placa',)  # Cambia a una tupla (nota la coma al final)
    list_filter = ('fecha_hora_ingreso', 'fecha_hora_salida')
    
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo_doc', 'num_doc', 'telefono', 'correo')
    search_fields = ('nombre', 'num_doc', 'correo')
    list_filter = ('tipo_doc',)
