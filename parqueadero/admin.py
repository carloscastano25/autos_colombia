from django.contrib import admin
from .models import CustomUser, Vehiculo, Celda, RegistroAsignacion, RegistroVehiculo

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id_persona', 'nombre', 'tipo_doc', 'num_doc', 'telefono', 'correo', 'user_type')
    search_fields = ('nombre', 'num_doc', 'correo')
    list_filter = ('user_type',)

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('id_vehiculo', 'placa', 'tipo_vehiculo', 'marca', 'color', 'propietario')
    search_fields = ('placa', 'marca', 'color')
    list_filter = ('tipo_vehiculo',)

@admin.register(Celda)
class CeldaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'disponible')
    list_filter = ('disponible',)

@admin.register(RegistroAsignacion)
class RegistroAsignacionAdmin(admin.ModelAdmin):
    list_display = ('empleado', 'usuario', 'vehiculo', 'celda', 'fecha_asignacion')
    search_fields = ('usuario__nombre', 'vehiculo__placa', 'celda__numero')

@admin.register(RegistroVehiculo)
class RegistroVehiculoAdmin(admin.ModelAdmin):
    list_display = ('vehiculo', 'fecha_hora_ingreso', 'fecha_hora_salida')
    search_fields = ('vehiculo__placa',)  # Cambia a una tupla (nota la coma al final)
    list_filter = ('fecha_hora_ingreso', 'fecha_hora_salida')
