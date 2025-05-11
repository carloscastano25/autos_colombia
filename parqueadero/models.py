from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now

# Modelo de Usuario Personalizado
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('administrador', 'Administrador'),
        ('empleado', 'Empleado'),
    )
    id_persona = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    tipo_doc = models.CharField(max_length=20, choices=[('CC', 'Cédula de Ciudadanía'), ('TI', 'Tarjeta de Identidad'), ('CE', 'Cédula de Extranjería')])
    num_doc = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    correo = models.EmailField(unique=True)
    user_type = models.CharField(max_length=15, choices=USER_TYPE_CHOICES, default='empleado')

    def __str__(self):
        return f"{self.nombre} ({self.get_user_type_display()})"

    def puede_registrar_empleados(self):
        return self.user_type == 'administrador'

    def puede_registrar_propietarios_y_vehiculos(self):
        return self.user_type in ['administrador', 'empleado']

# Modelo de Vehículo
class Vehiculo(models.Model):
    id_vehiculo = models.AutoField(primary_key=True)
    placa = models.CharField(max_length=10, unique=True)
    tipo_vehiculo = models.CharField(max_length=50, choices=[('Carro', 'Carro'), ('Moto', 'Moto'), ('Bicicleta', 'Bicicleta')])
    marca = models.CharField(max_length=50)
    color = models.CharField(max_length=30)
    propietario = models.CharField(max_length=100, blank=True, null=True)
    estado = models.BooleanField(default=False)  # False = "afuera", True = "adentro"

    def __str__(self):
        return f"{self.placa} - {self.tipo_vehiculo} ({self.marca}, {self.color})"

# Modelo de Celda
class Celda(models.Model):
    numero = models.CharField(max_length=10, unique=True)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"Celda {self.numero} - {'Disponible' if self.disponible else 'Ocupada'}"

# Modelo de Registro de Asignación ( Vehículo)
class RegistroAsignacion(models.Model):
    empleado = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='asignaciones', limit_choices_to={'user_type': 'empleado'})
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='clientes', limit_choices_to={'user_type': 'cliente'})
    vehiculo = models.OneToOneField(Vehiculo, on_delete=models.CASCADE)
    celda = models.OneToOneField(Celda, on_delete=models.CASCADE)
    fecha_asignacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Asignación: {self.usuario.nombre} - Vehículo: {self.vehiculo.placa} - Celda: {self.celda.numero}"

# Modelo de Registro de Ingreso y Salida
class RegistroVehiculo(models.Model):
    vehiculo = models.ForeignKey('Vehiculo', on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=[('entrada', 'Entrada'), ('salida', 'Salida')], default= 'salida')  # Campo tipo
    fecha_hora_ingreso = models.DateTimeField(blank=True, null=True)
    fecha_hora_salida = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.vehiculo.placa} - {self.tipo}"
